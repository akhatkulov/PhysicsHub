from . import db,login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    university = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))