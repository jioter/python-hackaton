from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import bcrypt
from .forms import (LoginForm, RegistrationForm)
from models import User
from flask_login import login_user, current_user, logout_user, login_required
from db import db
from app import login_manager
# from . import users

users = Blueprint('users', __name__, template_folder='templates')


# without API
@users.route("/signup", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(login=form.login.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your acc created! You can login", 'success')
        return redirect(url_for('users.login'))
    # return render_template('00_register.html')

    return render_template('00_register.html', title="Login", form=form)


@users.route("/login", methods=['GET', 'POST'])
# @login_manager.user_loader
def login():
    if current_user.is_authenticated:
        return redirect(url_for('game.games_page'))
    form = LoginForm()
    if form.validate_on_submit():
        # flash(f"Welcome, {form.username.data}!", 'success')
        # return redirect(url_for('main.home'))
        user = User.query.filter_by(login=form.login.data).first()
        # password = User.query.filter_by(password=form.password.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('game.games_page'))
        else:
            flash("Login Unsuccessful. Please, go home and die!", 'danger')
    return render_template('00_login.html', title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('game.games_page'))
