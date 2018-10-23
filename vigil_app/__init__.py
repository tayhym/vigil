import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

app.secret_key = os.urandom(12) # for running session with heroku instantiate outside 

db = SQLAlchemy(app)
db.create_all()
