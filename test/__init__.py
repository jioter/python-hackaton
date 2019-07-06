from flask import Blueprint, render_template


test = Blueprint('test', __name__, template_folder='templates')

@test.route("/")
def test():
    return render_template('test.html')

# @test.route("/test")
# def home_page():
#     """
#     # queries
#     https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
#
#     # select
#     user = User.query.filter_by(login="admin").first()
#
#     # insert
#     user = User(login="test", password="123", role=User.ROLE_USER)
#     db.session.add(user)
#     db.session.commit()
#
#     # delete
#     user = User.query.filter_by(login="test").first()
#     db.session.delete(user)
#     db.session.commit()
#     """
#
#     return render_template("test.html")
