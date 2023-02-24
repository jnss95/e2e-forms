from .. import db
import enum


class UserStatus(enum.Enum):
    ACTIVE = 1
    INACTIVE = 2
    DELETED = 3


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.Text())
    status = db.Column(db.Enum(UserStatus), default=UserStatus.INACTIVE)
    register_time = db.Column(db.DateTime(), default=db.func.now())
