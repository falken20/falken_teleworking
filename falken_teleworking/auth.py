# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/auth.py

from flask import Blueprint, render_template
from .models import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return 'login'

@auth.route('/signup')
def signup():
    return 'Signup'


@auth.route('/logout')
def logout():
    return 'Logout'
