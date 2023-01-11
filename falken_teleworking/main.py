# by Richi Rod AKA @richionline / falken20
# ./falken_quotes/main.py

from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv

from .logger import Log
from .config import get_settings

# Set environment vars
load_dotenv(find_dotenv())

app = Flask(__name__, template_folder="../templates",
            static_folder="../static")
app.config['TEMPLATE_AUTO_RELOAD'] = True

settings = get_settings()
Log.info(f"Settings: {settings}")


@app.route("/")
@app.route("/home")
def home():
    Log.info("Access to home page")

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
