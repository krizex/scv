import os
from flask import Flask
from scv import config

app = Flask(__name__)
# app.jinja_env.undefined = StrictUndefined


app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SECRET_KEY'] = os.urandom(24)

