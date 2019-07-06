from datetime import timedelta
from flask_wtf.csrf import CSRFProtect

# from auth import auth
<<<<<<< HEAD
# from game import game
# from test import test
=======
from game import game
from test import test
>>>>>>> 7bee9ff3c9c5b97e42c24bfda9b1eb4309be9a4d
from app import app
from db import db
from games.blueprint_games import games_b


def run_app():
    db.init_app(app)
    app.permanent_session_lifetime = timedelta(
        minutes=20)  # add session expire time

    # app.register_blueprint(test)
    # app.register_blueprint(auth)
<<<<<<< HEAD
    # app.register_blueprint(game)
    app.register_blueprint(games_b)
=======
    app.register_blueprint(game)

    CSRFProtect().init_app(app)
    app.config.update(dict(
        SECRET_KEY="xFiewikvWEkyHeXQ3iY6",
        WTF_CSRF_SECRET_KEY="yvggjVvE4yyMWHu2SsSKVCNwF0cXipuZaWWOqLLE"
    ))
>>>>>>> 7bee9ff3c9c5b97e42c24bfda9b1eb4309be9a4d

    return app


if __name__ == "__main__":
    run_app().run(debug=True)
