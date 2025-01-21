from flask import render_template, session, redirect, url_for, request, flash, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import SignInForm, SignUpForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route("/home")
def home_page():
    return "Hey"

@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            name = form.name.data
            surname = form.surname.data
            username = form.username.data
            university = form.university.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user:
                flash("Bu taxallusda foydalanuvchi mavjud.", "error")
                return redirect(url_for("main.signup"))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            new_user = User(name=name, surname=surname, username=username, university=university, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Ma\'lumotlar muvaffaqiyatli yuborildi!', 'success')
            return redirect(url_for("main.login_page"))

        except Exception as e:
            current_app.logger.error(f"Signup error: {e}")
            flash("Noma'lum xatolik yuz berdi, iltimos qayta urinib ko'ring.", "error")
            return redirect(url_for("main.signup"))
    return render_template('signup.html', form=form)

@main.route("/signin", methods=["GET", "POST"])
def login_page():
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.password and check_password_hash(user.password, password):
            login_user(user)
            flash("Kirish muvaffaqiyatli!", "success")
            return redirect(url_for('main.home_page'))

        flash("Taxallus yoki parol noto'g'ri", "error")
    return render_template("login.html", form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Siz muvaffaqiyatli chiqdingiz.", "success")
    return redirect(url_for('main.login_page'))
