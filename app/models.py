from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    university = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    messages = db.relationship('ChatMessage', backref='user', lazy=True)

    @hybrid_property
    def points(self):
        matter_points = (
            db.session.query(db.func.sum(MatterPoints.points_earned))
            .filter_by(user_id=self.id)
            .scalar()
            or 0
        )
        quiz_points = (
            db.session.query(db.func.sum(QuizPoints.points_earned))
            .filter_by(user_id=self.id)
            .scalar()
            or 0
        )
        return matter_points + quiz_points

    @hybrid_property
    def level(self):
        # Simple level formula: Level = (Points / 100) + 1
        return int(self.points / 100) + 1

    @hybrid_property
    def problems_solved(self):
        return (
            db.session.query(db.func.count(db.distinct(SolvedProblems.matter_id)))
            .filter_by(user_id=self.id)
            .scalar()
            or 0
        )

    @hybrid_property
    def tests_passed(self):
        return (
            db.session.query(db.func.count(db.distinct(TestResults.quiz_id)))
            .filter_by(user_id=self.id)
            .scalar()
            or 0
        )

    @hybrid_method
    def rank(self):
        subquery = db.session.query(
            User.id,
            db.func.coalesce(
                db.func.sum(MatterPoints.points_earned)
                + db.func.sum(QuizPoints.points_earned),
                0,
            ).label("total_points"),
        ).outerjoin(MatterPoints, User.id == MatterPoints.user_id)
        subquery = subquery.outerjoin(QuizPoints, User.id == QuizPoints.user_id)
        subquery = subquery.group_by(User.id).subquery()

        ranked_users = (
            db.session.query(subquery.c.id)
            .order_by(subquery.c.total_points.desc())
            .all()
        )
        rank_dict = {
            user_id: rank for rank, (user_id,) in enumerate(ranked_users, start=1)
        }
        return rank_dict.get(self.id, None)


class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(600), nullable=False)


class Matter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    main = db.Column(db.String(3600), nullable=False)
    helper = db.Column(db.String(600), nullable=False)
    correct = db.Column(db.String(100), nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True)
    ball = db.Column(db.Integer, nullable=False)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(36000), nullable=False)
    status = db.Column(db.Boolean, default=True)


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Gifs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(100), nullable=False)
    gif_path  = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    about = db.Column(db.String(10000), nullable=False)

class Labs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    about = db.Column(db.String(10000), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    pic_path = db.Column(db.String(1000), nullable=False)

class MatterPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    matter_id = db.Column(db.Integer, db.ForeignKey("matter.id"), nullable=True)
    points_earned = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("matter_progress", lazy=True))
    matter = db.relationship("Matter", backref=db.backref("solvers", lazy=True))


class QuizPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=True)
    points_earned = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("quiz_progress", lazy=True))
    quiz = db.relationship("Quiz", backref=db.backref("participants", lazy=True))

class SolvedProblems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    matter_id = db.Column(
        db.Integer, db.ForeignKey("matter.id"), nullable=False
    )


class TestResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(
        db.Integer, db.ForeignKey("quiz.id"), nullable=False
    )

class HandbookItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False) # e.g., 'Constants', 'Mechanics', 'Optics'
    title = db.Column(db.String(200), nullable=False)    # e.g., 'Gravity', 'Force Formula'
    content = db.Column(db.String(1000), nullable=False)  # e.g., 'g = 9.8 m/s^2', 'F = m * a'
    about = db.Column(db.String(1000), nullable=True)



def save_user_progress(user_id, item_id, points, x_type):
    if x_type == "matter":
        progress = MatterPoints.query.filter_by(
            user_id=user_id, matter_id=item_id
        ).first()
        if progress:
            progress.points_earned = points
        else:
            progress = MatterPoints(
                user_id=user_id, matter_id=item_id, points_earned=points
            )
            db.session.add(progress)

        if not SolvedProblems.query.filter_by(
            user_id=user_id, matter_id=item_id
        ).first():
            solved_problem = SolvedProblems(user_id=user_id, matter_id=item_id)
            db.session.add(solved_problem)

    elif x_type == "quiz":
        progress = QuizPoints.query.filter_by(user_id=user_id, quiz_id=item_id).first()
        if progress:
            progress.points_earned = points
        else:
            progress = QuizPoints(
                user_id=user_id, quiz_id=item_id, points_earned=points
            )
            db.session.add(progress)

        if not TestResults.query.filter_by(user_id=user_id, quiz_id=item_id).first():
            solved_test = TestResults(user_id=user_id, quiz_id=item_id)
            db.session.add(solved_test)

    else:
        raise ValueError("Invalid x_type. Use 'matter' or 'quiz'.")

    db.session.commit()


def check_history(user_id, item_id, x_type):
    result = {"status": False, "points": 0, "time": "never"}

    progress = None
    if x_type == "matter":
        progress = MatterPoints.query.filter_by(
            user_id=user_id, matter_id=item_id
        ).first()
    elif x_type == "quiz":
        progress = QuizPoints.query.filter_by(user_id=user_id, quiz_id=item_id).first()
    else:
        raise ValueError("Invalid x_type. Use 'matter' or 'quiz'.")

    if progress:
        result["status"] = True
        result["points"] = progress.points_earned
        if progress.timestamp:
            result["time"] = progress.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return result


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_leaderboard():
    subquery = (
        db.session.query(
            User.id,
            (
                db.func.coalesce(db.func.sum(MatterPoints.points_earned), 0)
                + db.func.coalesce(db.func.sum(QuizPoints.points_earned), 0)
            ).label("total_points"),
        )
        .outerjoin(MatterPoints, User.id == MatterPoints.user_id)
        .outerjoin(QuizPoints, User.id == QuizPoints.user_id)
        .group_by(User.id)
        .subquery()
    )

    top_users = (
        db.session.query(User, subquery.c.total_points)
        .join(subquery, User.id == subquery.c.id)
        .order_by(subquery.c.total_points.desc())
        .limit(10)
        .all()
    )

    return top_users


def get_all_themes():
    themes = Theme.query.all()
    return [{"id": t.id, "name": t.name, "about": t.about} for t in themes]

def get_animation_func_2():
    gifs = Gifs.query.all()
    return [
        {
            "id":g.id,
            'title':g.name,
            'theme':g.theme,
            "about":g.about,
            "gif_path":g.gif_path
        }
        for g in gifs
    ]

def get_matter_list():
    matters = Matter.query.all()
    return [
        {
            "id": m.id,
            "title": m.title.lower(),
            "main": m.main,
            "helper": m.helper,
            "correct": m.correct,
            "theme": m.theme,
            "status": m.status,
            "ball": m.ball,
        }
        for m in matters
    ]


def get_lab_list():
    labs = Labs.query.all()
    return [
        {
            "id": l.id,
            "title": l.name,
            "about": l.about,
            "link": l.link,
            "pic_path":l.pic_path
        }
        for l in labs
    ]

def get_all_quizzes():
    quizzes = Quiz.query.all()
    return [
        {
            "id": q.id,
            "title": q.title.lower(),
            "theme": q.theme,
            "data": q.data,
            "status": q.status,
        }
        for q in quizzes
    ]

def get_labs(prefix):
    labs = get_lab_list()
    return [q for q in labs if q["title"].startswith(prefix)]

def get_animation_func(prefix):
    gifs = get_animation_func_2()
    return [q for q in gifs if q["title"].startswith(prefix)]

def get_quiz(prefix):
    quizzes = get_all_quizzes()
    print("quizs", quizzes)
    return [q for q in quizzes if q["title"].startswith(prefix)]


def get_matter(prefix):
    matters = get_matter_list()
    return [m for m in matters if m["title"].startswith(prefix)]
