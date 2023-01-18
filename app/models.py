from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(255))
    member_since = db.Column(db.DateTime(), default=datetime.now)
    social_num1 = db.Column(db.Integer())
    social_num2 = db.Column(db.Integer())
    phone_num = db.Column(db.Integer())
    education = db.Column(db.Integer())
    radio = db.Column(db.Boolean())
    
