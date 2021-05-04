from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, UserMixin
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('Login.html')

@auth.route('/login', methods=['POST', 'GET'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Incorrect password, please try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.home'))

@auth.route('/signup')
def signup():
    return render_template('Sign_up.html')

@auth.route('/signup', methods=['POST', 'GET'])
def signup_post():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists!')
        return redirect(url_for('auth.signup')) #redirect user to login page if email already exists
    
    new_user = User(email=email, first_name=first_name, last_name=last_name, password = generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()  

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')
    