
from flask import Blueprint, render_template, redirect, url_for, request, flash
import flask_login
from . import db, bcrypt
from .models import User
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from .models import User
#from .forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import send_reset_email

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('Login.html')

@auth.route('/login', methods=['POST', 'GET'])
def login_post():
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials, please check your email and password')
            return redirect(url_for('auth.login'))
    return render_template('Login.html')
    """


    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if (email == None) or (password == None):
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()

    if user:
        if (bcrypt.check_password_hash(user.password, password)):
            login_user(user, remember=remember)
            return redirect(url_for('main.home'))
        else:
            flash('Incorrect password, please try again.')
            return redirect(url_for('auth.login'))
    else:
        flash('Invalid email address, please try again or sign up first.')
        return redirect(url_for('auth.login'))
    #if not user or not bcrypt.check_password_hash(user.password, password):


    #login_user(user, remember=remember)
    #return redirect(url_for('main.home'))



@auth.route('/signup')
def signup():
    return render_template('Sign_up.html')

@auth.route('/signup', methods=['POST', 'GET'])
def signup_post():
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You account has been registered!')
        return redirect(url_for('auth.login'))
    """
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    password_check = request.form.get('password1')
    
    if(email == None):
        flash("Please enter a valid email address!")                                                                                                                                                                                             
        return redirect(url_for('auth.signup'))

    if (password != password_check):
        flash('Password must be the same!')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists!')
        return redirect(url_for('auth.login')) #redirect user to login page if email already exists
    
    new_user = User(email=email, first_name=first_name, last_name=last_name, password = bcrypt.generate_password_hash(password).decode('utf-8'))

    db.session.add(new_user)
    db.session.commit()  

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


@auth.route('/reset_password')
def reset_request():
    return render_template('reset_request.html')

@auth.route('/reset_password', methods=['POST', 'GET'])
def reset_request_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    
    if user:
        send_reset_email(user)
        #flash("An email has been sent with instructions to reset your password.")
        return render_template('email_sent.html')
    else:
        flash("There is no account associated with that email address, please sign up first.")
        return redirect(url_for('auth.reset_request'))

    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
   
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.")
        return redirect(url_for('users.login'))
    return render_template('reset_request.html')
    """

@auth.route('/reset_password/<token>')
def reset_token(token):
    return render_template('reset_token.html')

@auth.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token_post(token):
    user = User.verify_reset_toke(token)

    if user is None:
        flash('This is an invalid or expired link, please retry.')
        return redirect(url_for('auth.reset_request'))
    password = request.form.get('password')
    password_check = request.form.get('password1')

    if (password != password_check):
        flash("password must be the same.")
        return render_template('reset_token.html')
    user.password = bcrypt.generate_password_hash(password).decode('utf=8')
    db.session.commit()
    flash('Your password has been updated.')
    return redirect(url_for('auth.login'))


    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('This is an invalid or expired link')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html')
    """

@auth.route('/profile')
@login_required
def profile():
    user_email = current_user.email
    return render_template('profile.html', current_email=user_email)

@auth.route('/profile', methods=['POST', 'GET'])
@login_required
def profile_post():
    #user = current_user
    user_email = current_user.email
    new_email = request.form.get('new_email')
    confirm_email = request.form.get('confirm_email')

    user = User.query.filter_by(email=new_email).first()
    if user:
        flash('Email address already exists!')
        return redirect(url_for('auth.profile_post')) #redirect user to login page if email already exists

    if (new_email == None):
        current_user.email = user_email

    elif (new_email != confirm_email):
        flash("email address must be the same.")
        return render_template('profile.html')
    else:
        current_user.email = confirm_email
        db.session.commit()
        flash('Your email address has been updated.')
        return redirect(url_for("auth.profile_post"))

    current_password = request.form.get('current_password')

    if (bcrypt.check_password_hash(current_user.password, current_password)):
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if(new_password != confirm_password):
            flash('Password must be the same')
            return redirect(url_for('auth.profile_post'))
        else:
            flash("Your password has been updated.")
            current_user.password = bcrypt.generate_password_hash(confirm_password).decode('utf=8')
            db.session.commit()
    else:
        flash('Incorrect password, please try again.')
        return redirect(url_for('auth.profile_post'))

    return redirect(url_for('auth.profile_post'))
