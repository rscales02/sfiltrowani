# coding=utf-8
"""
initialization of flask app for sfiltrowani
"""
from flask import Flask, request
from config import Config
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
import os
from flask_babel import lazy_gettext as _l

# create and configure an instance of class Flask
app = Flask(__name__)
app.config.from_object(Config)
# create user database
db = SQLAlchemy(app)
# implement ability to make changes to database
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
# implement email support
mail = Mail(app)
# implement bootstrap css framework
bootstrap = Bootstrap(app)
# implement time through moment.js
moment = Moment(app)
# implement translations
babel = Babel(app)


if not app.debug:
    """
    if not debugging, set up mail server and automatically email errors as they occur
    """
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/sfiltrowani.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from flaskr import routes, models, errors


@babel.localeselector
def get_locale():
    """
    find which languages are preferred by user and translate page into preferred language or best match
    :return: returns best match language to translate page into
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])
