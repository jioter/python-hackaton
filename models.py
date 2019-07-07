import datetime

from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin

from db import db
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
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

    DEFAULT_FROM_NUMBER = 0
    DEFAULT_TO_NUMBER = 10
    DEFAULT_ATTEMPTS = 3

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=backref('games', cascade="all,delete"))
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

    def is_inactive(self):
        return self.status == self.STATUS_INACTIVE

    def is_inprogress(self):
        return self.status == self.STATUS_PROGRESS


class GameResult(db.Model):
    __tablename__ = 'game_results'

    STATUS_NEW = 0
    STATUS_TRUE = 1
    STATUS_FALSE = 2

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    game = relationship('Game',
                        backref=backref('game_results', cascade="all,delete"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User',
                        backref=backref('game_results', cascade="all,delete"))
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

    @classmethod
    def create_result(cls, game_id, user_id):
        game_result = cls(
            game_id=game_id,
            user_id=user_id,
            retries=0
        )

        game = Game.query.get(game_id)
        game.status = Game.STATUS_PROGRESS

        db.session.add(game_result)
        db.session.commit()

        return game_result

    @classmethod
    def get_result(cls, game_id, user_id):
        game_result = cls.query.filter_by(
            game_id=game_id,
            status=cls.STATUS_NEW
        ).first()

        if not game_result:
            game_result = cls.create_result(game_id, user_id)

        return game_result

    def check_number(self, number):
        number = int(number)
        self.retries += 1

        if self.game.number == number:
            self.status = self.STATUS_TRUE
            self.date_finish = datetime.datetime.utcnow()
            self.game.status = Game.STATUS_INACTIVE
        elif self.game.attempts == self.retries:
            self.status = self.STATUS_FALSE
            self.date_finish = datetime.datetime.utcnow()
            self.game.status = Game.STATUS_ACTIVE

        db.session.commit()
