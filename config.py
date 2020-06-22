import os
basedir =os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kqwwieddkf2341sa'

    # Creates a database 'smart_home.db' on 
    # basedir path which is on the root of the application.
    # If it is created, then it's loaded
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://yakcahwxpbkpoq:4dca2e50c2d576037849f8c93c5d6c9e261b10c3e3e4252ad4a6706d314a02e5@ec2-54-86-170-8.compute-1.amazonaws.com:5432/d68g1hq5lbn38e' #or \
        #'sqlite:///' + os.path.join(basedir, 'smart_home.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False