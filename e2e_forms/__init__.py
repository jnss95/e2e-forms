from .auth import auth as auth_blueprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
print(app.config['ENV'])
app.config.from_pyfile('config.py')
if (app.config['DEBUG']):
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/lib/e2e-forms/e2e-forms.db'


db.init_app(app)

# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)


@app.route('/')
def hello():
    return 'Hello!'
