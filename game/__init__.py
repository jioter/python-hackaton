from flask import Blueprint, render_template, request, redirect, abort, url_for

from game.game_play_form import GamePlayForm
from models import Game, GameResult
from game.game_form import GameForm
from db import db

game = Blueprint("game", __name__, template_folder='templates')


@game.route("/", methods=["GET"])
def games_page():
    content = Game.query.order_by(
        Game.status.asc(),
        Game.date_created.desc()
    ).all()
    return render_template('games.html', content=content)


@game.route("/game/<int:game_id>", methods=["GET", "POST"])
def game_page(game_id):
    game = Game.query.get(int(game_id))
    # TODO - get real user_id
    user_id = 1

    if not game or game.status == Game.STATUS_INACTIVE:
        return render_template('game_inactive.html', game=game)

    form = GamePlayForm()
    game_results = GameResult.get_result(game_id, user_id)

    if game.status != Game.STATUS_ACTIVE and game_results.user_id != user_id:
        return render_template('game_inactive.html', game=game)

    if form.validate_on_submit():
        form.number.value = int(request.form.get('number'))
        game_results.check_number(form.number.value)

    if game_results.status == GameResult.STATUS_NEW:
        return render_template('game.html', form=form,
                               game_results=game_results)
    elif game_results.status == GameResult.STATUS_TRUE:
        return render_template('game_success.html', game_results=game_results)
    elif game_results.status == GameResult.STATUS_FALSE:
        return render_template('game_failed.html', game_results=game_results)


@game.route("/game-form", methods=["GET", "POST"])
@game.route("/game-form/<int:game_id>", methods=["GET", "POST", "DELETE"])
def game_form_page(game_id=None):
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
                return redirect(
                    url_for("game.game_form_page", game_id=game_id)
                )
            else:
                create_game()
                return redirect(url_for("game.games_page"))

        elif request.method == "POST" and request.form['_method'] == "DELETE":

            print(game_id)
            remove_game(game_id)

            return redirect(url_for("game.games_page"))

    return render_template('game_form.html', form=form, errors=errors)


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
