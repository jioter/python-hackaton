import datetime

from sqlalchemy import func
from sqlalchemy.orm import relationship, backref

from db import db


class User(db.Model):
    __tablename__ = 'users'

    ROLE_USER = 0
    ROLE_ADMIN = 1

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    role = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                             server_default=func.now())

    def __repr__(self):
        return f"id: {self.id}, login: {self.login}, role: {self.role}, " \
            f"date_created: {self.date_created}"


class Game(db.Model):
    __tablename__ = 'games'

    STATUS_ACTIVE = 0
    STATUS_PROGRESS = 1
    STATUS_INACTIVE = 2

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=backref('games', uselist=False))
    number = db.Column(db.Integer, nullable=False)
    from_number = db.Column(db.Integer, nullable=False)
    to_number = db.Column(db.Integer, nullable=False)
    attempts = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                             server_default=func.now())
    date_completed = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f"id: {self.id}, user: {self.user.login}, " \
            f"number: {self.number}, from_number: {self.from_number}, " \
            f"to_number: {self.to_number}, attempts: {self.attempts}, " \
            f"status: {self.status}, date_created: {self.date_created}, " \
            f"date_completed: {self.date_completed}"

    @classmethod
    def get_random_active_game(cls):
        return cls.query.filter_by(
            status=Game.STATUS_ACTIVE
        ).order_by(func.random()).limit(1).first()


class GameResult(db.Model):
    __tablename__ = 'game_results'

    STATUS_NEW = 0
    STATUS_TRUE = 1
    STATUS_FALSE = 2

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    game = relationship('Game', backref=backref('game_results', uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=backref('game_results', uselist=False))
    retries = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, default=0)
    date_start = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           server_default=func.now())
    date_finish = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f"game: {self.game.id}, user: {self.user.login}, " \
            f"retries: {self.retries}, status: {self.status}, " \
            f"date_start: {self.date_start}, date_finish: {self.date_finish}"
