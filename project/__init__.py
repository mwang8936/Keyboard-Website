from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'bigboobz'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587 #587 is the port for TLS: Transport Layer Security is a security protocol that encrypts email to protect its privacy
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = ekokeys2021@gmail.com
    app.config['MAIL_PASSWORD'] = bigboobz
    mail.init_app(app)

    db.init_app(app)

    bcrypt.init_app(app)

    #initializes a log in manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app