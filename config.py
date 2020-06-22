import os
basedir =os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kqwwieddkf2341sa'

    # Creates a database 'smart_home.db' on 
    # basedir path which is on the root of the application.
    # If it is created, then it's loaded
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'smart_home.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False