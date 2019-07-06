import datetime

from sqlalchemy.orm import relationship, backref

from db import db


class User(db.Model):
    __tablename__ = 'user'

    ROLE_USER = 0
    ROLE_ADMIN = 1

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    role = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Game(db.Model):
    __tablename__ = 'game'

    STATUS_ACTIVE = 0
    STATUS_PROGRESS = 1
    STATUS_INACTIVE = 2

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref=backref('user', uselist=False))
    number = db.Column(db.Integer, nullable=False)
    from_number = db.Column(db.Integer, nullable=False)
    to_number = db.Column(db.Integer, nullable=False)
    attempts = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_completed = db.Column(db.DateTime, default=None)


class GameResults(db.Model):
    __tablename__ = 'game_results'

    STATUS_NEW = 0
    STATUS_TRUE = 1
    STATUS_FALSE = 2

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    game = relationship('Game', backref=backref('game', uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref=backref('user', uselist=False))
    retries = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, default=0)
    date_start = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_finish = db.Column(db.DateTime, default=None)
