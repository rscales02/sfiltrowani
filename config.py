import os
basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
    # create class to configure flask app
    SECRET_KEY = os.environ.get('SECRET_KEY') or "that-is-a-secret"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
