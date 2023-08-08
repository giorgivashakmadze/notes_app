from . import db
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)

    @classmethod
    def create(cls, email, username, password):
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = cls(email=email, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
