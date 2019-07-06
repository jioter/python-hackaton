from flask import Blueprint
from flask_restful import Api
from app.game.routes import Game

game = Blueprint("game", __name__)
api = Api(game)

api.add_resource(Game, "/game")
