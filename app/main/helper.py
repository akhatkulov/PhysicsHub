from werkzeug.security import generate_password_hash

def create_user(username, name, surname, university, password):
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, name=name, surname=surname, university=university, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user