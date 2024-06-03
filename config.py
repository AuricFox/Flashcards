'''
Flask App configuration

To set the configuration type, navigate to __init__.py file in the 
app directory and change the configuration in the init_app function

Using a production configuration:
app.config.from_object('config.ProdConfig')

Using a development configuration:
app.config.from_object('config.DevConfig')

Configuration Variables:

FLASK_DEBUG: provides logging for debugging purposes
SECRET_KEY: strings used to encrypt sensitive data
SERVER_NAME: app's domian name

More Info:
https://flask.palletsprojects.com/en/3.0.x/config/
'''

from os import environ, path
from dotenv import load_dotenv

BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, '.env'))

class Config:
    '''
    Base config
    '''
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    SECRET_KEY = environ.get('SECRET_KEY') or 'df0331cefc6c2b9a5dserknvwier726a5d1c0fd37324feba25506'

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')\
        or 'sqlite:///' + path.join(BASEDIR, './data/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    '''
    Production config
    '''
    FLASK_ENV = "production"


class DevConfig(Config):
    '''
    Development config
    '''
    FLASK_ENV = "development"
    FLASK_DEBUG = True

class TestingConfig(Config):
    '''
    Testing config
    '''
    FLASK_ENV = "testing"
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URI')\
        or 'sqlite:///' + path.join(BASEDIR, './data/app_test.db')