import os
from typing import Tuple
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash

import scrypt
from base64 import b64encode, b64decode

from e2e_forms.models.user import User, UserStatus
from . import db
from . import app

auth = Blueprint('auth', __name__)

def hash_password(password: str) -> bytes:
    """Hash a password for storing.
    :param password: The password to hash.
    :return: A chunk of random bytes encrypted with the password."""
    salt = os.urandom(app.config['SCRYPT_SALT_LENGTH'])
    return scrypt.encrypt(salt, password.encode('utf-8'), app.config['SCRYPT_MAX_TIME'])


def verify_password(password: str, hashed_password: bytes) -> bool:
    """Verify a password against a stored hash.
    :param password: The password to verify.
    :param hashed_password: The stored password hash to compare against.
    :return: True if the password matches the stored hash, False otherwise."""
    try:
        scrypt.decrypt(hash_password, password.encode('utf-8'), app.config['SCRYPT_MAX_TIME'])
        return True
    except scrypt.error:
        return False
    return False

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
    password = request.form.get('password')
    password = request.form.get('password_repeat')

    user = User.query.filter_by(email=email).first()


    if user:
        if user.status == UserStatus.ACTIVE:
            flash('Email address already exists')
            return render_template('auth/signup.html')
        db.sesion.delete(user)          

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    hashed_password = hash_password(password)
    new_user = User(email=email, password=b64encode(hashed_password).decode('utf-8'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return render_template("notice.html", notice="To complete your registration, please check your email for a confirmation link.")

@auth.route('/logout')
def logout():
    return 'Logout'