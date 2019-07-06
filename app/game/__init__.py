from flask import Blueprint
from flask_restful import Api
from game.routes import Game

game = Blueprint("game", __name__)
api = Api(auth)

api.add_resource(Game, "/game")
