from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


from .auth import users
# from game import game
from .test import test
from .app import app
from .db import db


bcrypt = Bcrypt()  # for password hashing
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def run_app():

    db.init_app(app)
    app.permanent_session_lifetime = timedelta(
        minutes=20)  # add session expire time

    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(test)
    app.register_blueprint(users)
    # app.register_blueprint(auth)
    # app.register_blueprint(game)

    return app


if __name__ == "__main__":
    run_app().run(debug=True)
