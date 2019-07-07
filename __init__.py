from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from app import bcrypt, login_manager

from auth.routes import users
from game import game
from app import app
from db import db


def run_app():
    db.init_app(app)
    app.permanent_session_lifetime = timedelta(
        minutes=20)  # add session expire time

    # app.register_blueprint(test)
    app.register_blueprint(users)
    app.register_blueprint(game)

    CSRFProtect().init_app(app)
    app.config.update(dict(
        SECRET_KEY="xFiewikvWEkyHeXQ3iY6",
        WTF_CSRF_SECRET_KEY="yvggjVvE4yyMWHu2SsSKVCNwF0cXipuZaWWOqLLE"
    ))

    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app


if __name__ == "__main__":
    run_app().run(debug=True)
