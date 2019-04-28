import os
from flask import Flask, jsonify, abort, make_response, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from urllib.parse import urlparse


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path="")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'aksdjfi%@$%@$%QERRF%^WFd8745hds!#@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_APP'] = 'app.py'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
auth = HTTPBasicAuth()

class Domain(db.Model):
    __tablename__ = 'domain'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(256), index=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


class DomainAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        url = request.args.get('url')
        parsed_uri = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        print(result)

        dom_in_db = Domain.query.filter_by(domain=result).first()
        print(dom_in_db)
        if dom_in_db is None:
            return jsonify({'is_safe':True})
        else:
            return jsonify({'is_safe':False})


class TokenAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        token = g.user.generate_auth_token(600)
        return jsonify({'token': token.decode('ascii'), 'duration': 600})


api.add_resource(DomainAPI, '/api/v1.0/domain')
api.add_resource(TokenAPI, '/api/v1.0/token')

if __name__ == '__main__':
    app.run()
    # db requires flask db init, upgrade and update
