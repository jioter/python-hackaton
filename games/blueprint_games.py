from flask import Flask, render_template, Blueprint
from functools import wraps
from flask import g, request, redirect, url_for
from models import Game, User

games_b = Blueprint('games', __name__, template_folder='templates')

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('/', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function



@games_b.route('/games')
# @login_required
def games():
    content = Game.query.order_by(Game.status).all()
    return render_template('games.html', content=content)

@games_b.route('/games/<game_id>')
def game(game_id):
    return render_template('game.html',  )




