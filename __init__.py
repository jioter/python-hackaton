from datetime import timedelta
from flask_wtf.csrf import CSRFProtect

# from auth import auth
from game import game
from test import test
from app import app
from db import db


def run_app():
    db.init_app(app)
    app.permanent_session_lifetime = timedelta(
        minutes=20)  # add session expire time

    app.register_blueprint(test)
    # app.register_blueprint(auth)
    app.register_blueprint(game)

    CSRFProtect().init_app(app)
    app.config.update(dict(
        SECRET_KEY="xFiewikvWEkyHeXQ3iY6",
        WTF_CSRF_SECRET_KEY="yvggjVvE4yyMWHu2SsSKVCNwF0cXipuZaWWOqLLE"
    ))

    return app


if __name__ == "__main__":
    run_app().run(debug=True)
