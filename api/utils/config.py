from os import environ
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CHURCH_AUTH_URL = "http://mvsongs.co.za/api"
    if environ.get('CHURCH_AUTH_URL'):
        CHURCH_AUTH_URL = environ.get('CHURCH_AUTH_URL')

    CHURCH_SONGS_URL = "http://mvsongs.co.za/api"
    if environ.get('CHURCH_SONGS_URL'):
        CHURCH_SONGS_URL = environ.get('CHURCH_SONGS_URL')

    CHURCH_API_USERNAME = "worship"
    if environ.get('CHURCH_API_USERNAME'):
        CHURCH_API_USERNAME = environ.get('CHURCH_API_USERNAME')

    CHURCH_API_PASSWORD = "password"
    if environ.get('CHURCH_API_PASSWORD'):
        CHURCH_API_PASSWORD = environ.get('CHURCH_API_PASSWORD')

    SONGBOOK_TMP_DIR = "./temp"
    if environ.get('SONGBOOK_TMP_DIR'):
        SONGBOOK_TMP_DIR = environ.get('SONGBOOK_TMP_DIR')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ECHO = False
