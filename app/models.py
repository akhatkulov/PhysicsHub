from . import db,login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    university = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(100),nullable=False)
    about = db.Column(db.String(600),nullable=False)

class Matter(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(80),nullable=False)
    main = db.Column(db.String(3600),nullable=False)
    helper = db.Column(db.String(600),nullable=False)
    correct = db.Column(db.String(100),nullable=False)
    theme = db.Column(db.String(100),nullable=False)
    status = db.Column(db.Boolean,default=True)

class Quiz(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(80),nullable=False)
    theme = db.Column(db.String(100),nullable=False)
    data = db.Column(db.String(36000),nullable=False)
    status = db.Column(db.Boolean,default=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_all_themes():
    themes = Theme.query.all()
    return [{'id': t.id, 'name': t.name, 'about': t.about} for t in themes]
