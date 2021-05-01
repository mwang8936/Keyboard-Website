from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/profile')
def profile():
    return 'Profile'

