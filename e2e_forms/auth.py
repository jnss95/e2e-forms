import os
from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from scrypt import hash as scrypt_hash

from e2e_forms.models.user import User
from . import db

auth = Blueprint('auth', __name__)

def hash_password(password):
    #generate random salt
    salt = os.urandom(32)
    return (salt, scrypt_hash(password, salt, maxtime=0.1))

def verify_password(password, salt, hashed_password):
    return scrypt_hash(password, salt) == hashed_password

@auth.route('/login')
def login():
    return 'Login'

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=hash_password(password))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

@auth.route('/logout')
def logout():
    return 'Logout'