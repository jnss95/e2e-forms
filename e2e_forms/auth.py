import os
import scrypt
from flask_wtf import FlaskForm
from wtforms.fields import EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from flask import Blueprint, flash, render_template, request
from base64 import b64encode

from e2e_forms.models.user import User, UserStatus
from e2e_forms import db
from e2e_forms import app

auth = Blueprint('auth', __name__)


class SignupForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(
                max=255)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField(
        'Repeat Password', validators=[
            DataRequired(), EqualTo(
                'password', message='Passwords must match')])


def hash_password(password: str) -> bytes:
    """Hash a password for storing.
    :param password: The password to hash.
    :return: A chunk of random bytes encrypted with the password."""
    salt = os.urandom(app.config['SCRYPT_SALT_LENGTH'])
    return scrypt.encrypt(salt, password.encode('utf-8'),
                          app.config['SCRYPT_MAX_TIME'])


def verify_password(password: str, hashed_password: bytes) -> bool:
    """Verify a password against a stored hash.
    :param password: The password to verify.
    :param hashed_password: The stored password hash to compare against.
    :return: True if the password matches the stored hash, False otherwise."""
    try:
        scrypt.decrypt(hash_password, password.encode('utf-8'),
                       app.config['SCRYPT_MAX_TIME'])
        return True
    except scrypt.error:
        return False
    return False


@auth.route('/login')
def login():
    return 'Login'


@auth.route('/signup')
def signup():
    form = SignupForm()
    return render_template('auth/signup.html', form=form)


@auth.route('/signup', methods=['POST'])
def signup_post():
    form = SignupForm()
    if not form.validate_on_submit():
        return render_template('auth/signup.html', form=form)
    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()
    if user:
        if user.status == UserStatus.ACTIVE:
            flash('Email address already exists')
            return render_template('auth/signup.html')
        # User exists but never activated its account.
        db.sesion.delete(user)

    hashed_password = hash_password(password)
    new_user = User(email=email,
                    password=b64encode(hashed_password).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return render_template("notice.html",
                           notice="To complete your registration, "
                                  "please check your email for "
                                  "a confirmation link.")


@auth.route('/logout')
def logout():
    return 'Logout'
