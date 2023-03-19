import os
from decouple import config
from datetime import timedelta
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', 'mysecrets')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN = timedelta(minutes=30)
    JWT_SECRET_KEY = 'e52967e0f574'



class DevConfig(Config):
    # DEBUG = config('DEBUG',cast=bool)
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'enrollment.db')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class ProdConfig(Config):
    pass

config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}