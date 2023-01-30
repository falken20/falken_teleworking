# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/main.py

from .auth import auth as auth_blueprint
from flask import Blueprint, render_template, request
from dotenv import load_dotenv, find_dotenv
import os
from datetime import datetime

from .logger import Log, console
from .config import get_settings
from .models import Teleworking, db

main = Blueprint('main', __name__)


@main.route("/", methods=('GET', 'POST'))
@main.route("/home", methods=('GET', 'POST'))
def index():
    Log.info("Access to home page")

    if request.method == "POST" and request.form.get('work_home') is not None:
        Log.info("Saving the day info...")
        Teleworking.create_day(request.form)

    count_home = Teleworking.get_count_days("true")
    count_office = Teleworking.get_count_days("false")
    percent = round(count_office / (count_home + count_office) * 100, 2)

    checked_home, checked_office = None, None
    if Teleworking.get_day(datetime.now().date()):
        if (Teleworking.get_day(datetime.now().date())).work_home:
            checked_home = "checked"
        else:
            checked_office = "checked"

    return render_template("index.html",
                           day=datetime.now().date(),
                           count_home=count_home,
                           count_office=count_office,
                           percent=percent,
                           checked_home=checked_home,
                           checked_office=checked_office)


@main.route('/profile')
def profile():
    return render_template('profile.html')


