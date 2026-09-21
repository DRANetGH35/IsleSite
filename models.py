from flask_login import UserMixin
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    email: Mapped[str] = mapped_column(String(1000))
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verified: Mapped[int] = mapped_column(Integer, nullable=False)
    verification_code: Mapped[int] = mapped_column(Integer, nullable=False)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(name=username).first()

    @classmethod
    def exists(cls, name):
        return cls.query.filter_by(name=name).first() is not None

    @classmethod
    def password_correct(cls, username, password):
        return check_password_hash(cls.get_by_username(username).password, password)