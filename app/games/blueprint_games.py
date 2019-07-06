from flask import Flask, render_template, Blueprint
from functools import wraps
from flask import g, request, redirect, url_for

games_b = Blueprint('games', __name__, template_folder='templates')

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('/', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function


content = {'game_1': 'user1',
           'game_2': 'user2',
           'game_3': 'user3',
           'game_4': 'user4',
           'game_5': 'user5'}

@games_b.route('/games')
# @login_required
def games():
    return render_template('games.html', content=content)

@games_b.route('/games/<game_id>')
def game(game_id):
    return render_template('game.html', game=content.get(game_id))




