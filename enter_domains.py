from app import app
from app import db
from app import Domain
import os

with app.app_context():
    domain = Domain(domain='http://appleid.apple.com-signin.2qbpwdtf568zwts0n8kgcrhlq88kq6.com/')
    db.session.add(domain)
    domain = Domain(domain='https://www.pinkheater.com/')
    db.session.add(domain)
    domain = Domain(domain='http://tetracebu.com/')
    db.session.add(domain)
    domain = Domain(domain='http://help-sec55.ml/')
    db.session.add(domain)
    domain = Domain(domain='https://ww10.todamae-merece.com/')
    db.session.add(domain)
   
    db.session.commit()
    print("Domains created")
    