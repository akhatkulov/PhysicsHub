from werkzeug.security import generate_password_hash
from .. import db
from ..models import User


def create_user(username, name, surname, university, password):
    new_user = User(
        username=username,
        name=name,
        surname=surname,
        university=university,
        password=generate_password_hash(password, method='pbkdf2:sha256'),
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user
