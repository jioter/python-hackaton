from flask import Blueprint, render_template, request, redirect
from models import Game
from game.game_form import GameForm
from db import db

game = Blueprint("game", __name__, template_folder='templates')


@game.route("/game", methods=["GET", "POST", "DELETE"])
def game_page():
    form = GameForm()
    errors = None
    if form.is_submitted() and not form.validate():
        errors = form.errors

    if request.method == "POST" and request.form['_method'] == "POST":
        result = create_game()
        if result:
            return redirect('/')

    elif request.method == "POST" and request.form['_method'] == "DELETE":
        remove_game()

    return render_template('form.html', form=form, errors=errors)


def update_game():
    pass


def create_game():
    from_number = request.form.get('from_number') or 0
    to_number = request.form.get('to_number') or 10
    attempts = request.form.get('attempts') or 3

    new_game = Game(
        number=request.form['number'],
        user_id=request.form['user_id'],
        from_number=from_number,
        to_number=to_number,
        attempts=attempts,
        status=Game.STATUS_ACTIVE
    )

    db.session.add(new_game)
    db.session.commit()

    return new_game.id


def remove_game():
    pass
