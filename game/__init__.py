from flask import Blueprint
from flask_restful import Api

game = Blueprint("game", __name__)


@game.route("/game", methods=["GET", "POST", "DELETE"])
def game_page():
    # if request.method == "POST" and request.form['_method'] == "POST":
    #     if request.form['id']:
    #         update_fruit()
    #     else:
    #         create_fruit()
    # elif request.method == "POST" and request.form['_method'] == "DELETE":
    #     remove_fruit()

    return 'Game'


def update_fruit():
    pass


def create_fruit():
    pass


def remove_fruit():
    pass
