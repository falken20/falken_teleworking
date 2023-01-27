# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/models.py

# ######################################################################
# This file is to set all the db models and use the ORM flask_sqlalchemy
# With this file it is no neccesary to use prices.py and products.py
# ######################################################################


from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv, find_dotenv

# from src.logger import Log
import logging
from .logger import Log

FORMAT = '%(asctime)s %(levelname)s %(lineno)d %(filename)s %(funcName)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# Load .env file
load_dotenv(find_dotenv())

# Create db object
db = SQLAlchemy()


class Teleworking(db.Model):
    # Table name in class name in camel_case. You can override with __tablename__
    __tablename__ = "t_teleworking"

    work_date = db.Column(db.Date, primary_key=True)
    work_home = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f"Day: {self.work_date} / Work Home: {self.work_home}"

    @staticmethod
    def get_all_days():
        return Teleworking.query.order_by(Teleworking.work_date.desc()).all()

    @staticmethod
    def get_count_days(work_home):
        """ Return count days working at home (true) or office (false) """
        return len(Teleworking.query.filter_by(work_home=work_home).all())

    @staticmethod
    def get_day(work_date):
        return Teleworking.query.filter_by(work_date=work_date).first()

    @staticmethod
    def delete_day(work_date):
        Teleworking.query.filter_by(work_date=work_date).delete()
        db.session.commit()

    @staticmethod
    def create_day(values):
        Log.info("Saving info day in DB...")
        # Delete the day if exists
        Teleworking.delete_day(datetime.now().date())

        new_teleworking = Teleworking(
            work_date=datetime.now().date(),
            work_home=True if values.get('work_home') == "True" else False,
        )

        db.session.add(new_teleworking)
        db.session.commit()

        return new_teleworking


def init_db(app):
    """
    Main process to create the needed tables for the application
    """
    logging.info("Init DB process starting...")

    try:
        if input("Could you drop the tables if they exist(y/n)? ") in ["Y", "y"]:
            with app.app_context():
                db.drop_all()
            logging.info("Tables dropped")

        if input("Could you create the tables(y/n)? ") in ["Y", "y"]:
            logging.info("Creating tables...")
            with app.app_context():
                db.create_all()

        with app.app_context():
            db.session.commit()

        logging.info("Process finished succesfully")

    except Exception as err:
        logging.error(f"Execution Error in init_db: {err}", exc_info=True)


if __name__ == '__main__':
    logging.info("Preparing app vars...")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
        "://", "ql://", 1)
    db.init_app(app)
    init_db(app)
