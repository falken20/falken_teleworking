# by Richi Rod AKA @richionline / falken20
# ./falken_quotes/main.py

from .auth import auth as auth_blueprint
from flask import Flask, render_template, request
from dotenv import load_dotenv, find_dotenv
import os
from datetime import datetime

from .logger import Log, console
from .config import get_settings
from .models import Teleworking, db

# Set environment vars
load_dotenv(find_dotenv())

console.rule("Falken Teleworking")
settings = get_settings()
Log.info(f"Settings: {settings}")

app = Flask(__name__, template_folder="../templates",
            static_folder="../static")
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
    "://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

# Register blueprint for auth features
app.register_blueprint(auth_blueprint)


@app.route("/", methods=('GET', 'POST'))
@app.route("/home", methods=('GET', 'POST'))
def home():
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


if __name__ == "__main__":
    app.run()
