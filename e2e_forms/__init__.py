

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

# autopep8: off
app = Flask(__name__)
db = SQLAlchemy()
from e2e_forms.auth import auth as auth_blueprint
babel = Babel(app)
print(app.config['ENV'])
app.config.from_pyfile('config.py')
if (app.config['DEBUG']):
    app.config['SECRET_KEY'] = 'dev'
# autopep8: on

db.init_app(app)

# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)


@app.route('/')
def hello():
    return 'Hello!'
