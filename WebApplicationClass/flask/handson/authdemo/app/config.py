import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'FBu3JeeUzO_jhgVT_XlYWbarA2bjKR3L'
    #
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'authdemo.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
         'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
