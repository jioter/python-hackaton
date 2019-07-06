from flask import Blueprint, render_template

test = Blueprint('test', __name__, template_folder='templates')


@test.route("/test")
def home_page():
    return render_template("test.html")
