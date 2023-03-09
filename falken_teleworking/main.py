# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/main.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from functools import lru_cache

from .logger import Log
from .models import Teleworking, User
from .config import get_settings

main = Blueprint('main', __name__)

previous_cache = datetime.now()


@main.route("/", methods=('GET', 'POST'))
@main.route("/home", methods=('GET', 'POST'))
@login_required
def index():
    Log.info("Access to home page")
    Log.debug(f"Current user: {current_user.name}")
    Log.debug(f"Date to calculate period percent: {current_user.date_from}")

    if request.method == "POST" and request.form.get('work_home') is not None:
        Log.info("Saving the day info...")
        Teleworking.create_day(request.form, current_user.id)

    count_home = Teleworking.get_count_days(
        True, current_user.id, current_user.date_from)
    count_office = Teleworking.get_count_days(
        False, current_user.id, current_user.date_from)
    if (count_home + count_office != 0):
        percent = round(count_office / (count_home + count_office) * 100, 2)
    else:
        percent = 0

    checked_home, checked_office = None, None
    if Teleworking.get_day(datetime.now().date(), current_user.id):
        if (Teleworking.get_day(datetime.now().date(), current_user.id)).work_home:
            checked_home = "checked"
        else:
            checked_office = "checked"

    check_cache()

    return render_template("index.html",
                           day=datetime.now().date(),
                           count_home=count_home,
                           count_office=count_office,
                           percent=percent,
                           checked_home=checked_home,
                           checked_office=checked_office,
                           date_from=current_user.date_from,
                           user=current_user.name)


@main.route('/profile')
@login_required
def profile():
    date_from = current_user.date_from
    return render_template('profile.html', name=current_user.name, date_from=date_from)


@main.route('/profile', methods=['POST'])
@login_required
def profile_post():
    Log.info("Saving profile data...")
    date_from = request.form.get('date_from')
    User.update_user_date(current_user.id, date_from)
    return redirect(url_for('main.index'))


@main.route('/calendar')
@login_required
def calendar():
    # Get all date fields for fullfill calendar
    all_dates = calendar_data(current_user.id)
    Log.debug(all_dates)
    return render_template('calendar.html', all_dates=all_dates)


@lru_cache(maxsize=0)
def calendar_data(user_id):
    return Teleworking.get_all_dates(user_id, current_user.date_from)


def check_cache(minutes: int = 60):
    # Cache info:
    # hits is the number of calls that @lru_cache returned directly from memory because they existed in the cache.
    # misses is the number of calls that didn’t come from memory and were computed.
    # maxsize is the size of the cache as you defined it with the maxsize attribute of the decorator.
    # currsize  is the current size of the cache.
    global previous_cache
    Log.info(
        f"CACHE calendar_data(): {calendar_data.cache_info()}", style="yelloW")
    Log.info(
        f"CACHE get_settings(): {get_settings.cache_info()}", style="yelloW")
    Log.info(
        f"Checking expiration time for cache({minutes=})...", style="yellow")
    Log.debug(f"Previous cache: {previous_cache}", style="yellow")
    Log.debug(f"Current time: {datetime.now()}", style="yellow")
    difference = (datetime.now() - previous_cache).seconds / 60
    Log.info(f"Cache span: {int(difference)} minutes", style="yellow")
    if difference > minutes:
        Log.info("Cleaning cache by expiration...", style="yellow")
        calendar.cache_clear()
        previous_cache = datetime.now()
        Log.info(f"CACHE: {calendar.cache_info()}", style="yellow")
