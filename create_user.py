from app import app
from app import db
from app import User
import os

with app.app_context():
    user = User(username=os.environ.get('API_USERNAME') or 'admin')
    user.hash_password(os.environ.get('API_PASSWORD') or 'class')
    db.session.add(user)
    db.session.commit()
    print("User created")
    