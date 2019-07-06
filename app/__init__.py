from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask

from .auth.routes import users
# from app.game import game
# from app.app import app

bcrypt = Bcrypt()  # for password hashing
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def run_app():
    app = Flask(__name__, static_url_path='/static')

    db.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=20)  # add session expire time

    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(users)
    # app.register_blueprint(game)

    return app


if __name__ == "__main__":
    run_app().run(debug=True)
