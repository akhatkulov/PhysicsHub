from flask import Flask, jsonify, request, redirect, url_for
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config

mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login_page"
login_manager.login_message = "Iltimos, avval tizimga kiring."
csrf = CSRFProtect()


@login_manager.unauthorized_handler
def _unauthorized():
    if request.path.startswith("/api/") or request.path.startswith("/admin/"):
        return jsonify({"error": "Authentication required"}), 401
    return redirect(url_for(login_manager.login_view, next=request.url))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
