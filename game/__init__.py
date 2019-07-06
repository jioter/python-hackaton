from flask import Blueprint, render_template, request, redirect, abort
from models import Game
from game.game_form import GameForm
from db import db

game = Blueprint("game", __name__, template_folder='templates')


@game.route("/", methods=["GET"])
def games():
    content = Game.query.order_by(Game.status).all()
    return render_template('games.html', content=content)


@game.route("/game", methods=["GET", "POST"])
@game.route("/game/<int:game_id>", methods=["GET", "POST", "DELETE"])
def game_page(game_id=None):
    game = None
    if game_id:
        game = Game.query.get(int(game_id))
        if not game:
            abort(404)

    form = GameForm()
    if game:
        form.id.value = game.id
        form.number.value = game.number
        form.from_number.value = game.from_number
        form.to_number.value = game.to_number
        form.attempts.value = game.attempts
    else:
        form.from_number.value = Game.DEFAULT_FROM_NUMBER
        form.to_number.value = Game.DEFAULT_TO_NUMBER
        form.attempts.value = Game.DEFAULT_ATTEMPTS

    errors = None
    if form.is_submitted() and not form.validate():
        errors = form.errors

    if not errors:
        if request.method == "POST" and request.form['_method'] == "POST":
            if game_id:
                update_game(game_id)
            else:
                create_game()

            return redirect('/')
        elif request.method == "POST" and request.form['_method'] == "DELETE":
            remove_game(game_id)

            return redirect('/')

    return render_template('form.html', form=form, errors=errors)


def update_game(game_id):
    from_number = request.form.get('from_number') or Game.DEFAULT_FROM_NUMBER
    to_number = request.form.get('to_number') or Game.DEFAULT_TO_NUMBER
    attempts = request.form.get('attempts') or Game.DEFAULT_ATTEMPTS

    game = Game.query.get(int(game_id))
    game.number = request.form['number']
    game.from_number = from_number
    game.to_number = to_number
    game.attempts = attempts

    db.session.commit()


def create_game():
    from_number = request.form.get('from_number') or Game.DEFAULT_FROM_NUMBER
    to_number = request.form.get('to_number') or Game.DEFAULT_TO_NUMBER
    attempts = request.form.get('attempts') or Game.DEFAULT_ATTEMPTS

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


def remove_game(game_id):
    game = Game.query.get(int(game_id))

    db.session.delete(game)
    db.session.commit()
