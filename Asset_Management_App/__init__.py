#Asset_Management_App/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:csemavs@localhost/AssetManager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_TYPE'] = 'sqlalchemy'

app.config.from_object('config')

db = SQLAlchemy(app)

from Asset_Management_App import views




