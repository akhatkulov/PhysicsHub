from . import db,login_manager
from flask_login import UserMixin
import datetime

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

class MatterPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    matter_id = db.Column(db.Integer, db.ForeignKey('matter.id'), nullable=True)  
    points_earned = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) 
    user = db.relationship('User', backref=db.backref('progress', lazy=True))
    matter = db.relationship('Matter', backref=db.backref('solvers', lazy=True))

class QuizPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=True) 
    points_earned = db.Column(db.Integer, nullable=False)  
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('progress', lazy=True))
    quiz = db.relationship('Quiz', backref=db.backref('participants', lazy=True))

def save_user_progress(user_id, item_id, points, x_type):
    if x_type == "matter":
        progress = MatterPoints.query.filter_by(user_id=user_id, matter_id=item_id).first()
        
        if progress:
            progress.points_earned = points
            progress.timestamp = datetime.utcnow()
        else:
            progress = MatterPoints(user_id=user_id, matter_id=item_id, points_earned=points)
            db.session.add(progress)

    elif x_type == "quiz":
        progress = QuizPoints.query.filter_by(user_id=user_id, quiz_id=item_id).first()

        if progress:
            progress.points_earned = points
            progress.timestamp = datetime.utcnow()
        else:
            progress = QuizPoints(user_id=user_id, quiz_id=item_id, points_earned=points)
            db.session.add(progress)

    else:
        raise ValueError("Invalid x_type. Use 'matter' or 'quiz'.")

    db.session.commit()

def check_history(user_id, item_id, x_type):
    result = {'status': False, 'points': 0, 'time': "never"}

    if x_type == "matter":
        progress = MatterPoints.query.filter_by(user_id=user_id, matter_id=item_id).first()
    elif x_type == "quiz":
        progress = QuizPoints.query.filter_by(user_id=user_id, quiz_id=item_id).first()
    else:
        raise ValueError("Invalid x_type. Use 'matter' or 'quiz'.")

    if progress:
        result['status'] = True
        result['points'] = progress.points_earned
        result['time'] = progress.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return result

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_all_themes():
    themes = Theme.query.all()
    return [{'id': t.id, 'name': t.name, 'about': t.about} for t in themes]
