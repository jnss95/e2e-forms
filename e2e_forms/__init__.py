from flask import Flask, request,g 
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
import sqlite3
app = Flask(__name__)
db = SQLAlchemy()
print(app.config['ENV'])
if (app.config['ENV'] == 'dev'):
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/lib/e2e-forms/e2e-forms.db'



db.init_app(app)

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

@app.route('/')
def hello():
    return f'Hello!'

