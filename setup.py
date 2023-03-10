from setuptools import setup

setup(
    name='e2e-forms',
    packages=['e2e-forms'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-login',
        'scrypt',
        'Flask-WTF',
        'email_validator',
        'Flask-Babel'
    ],
)
