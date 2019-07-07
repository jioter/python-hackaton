from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

bcrypt = Bcrypt()  # for password hashing
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html'), 404
