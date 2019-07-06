from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskblog import, bcrypt
from flaskblog.users.forms import (LoginForm, RegistrationForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm)
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, save_post_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your acc created! You can login", 'success')
        return redirect(url_for('users.login'))
    return render_template('00_register.html', title="Login-admin", form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # flash(f"Welcome, {form.username.data}!", 'success')
        # return redirect(url_for('main.home'))
        user = User.query.filter_by(email=form.email.data).first()
        # password = User.query.filter_by(password=form.password.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful. Please, go home and die!", 'danger')
    return render_template('00_login.html', title="Login-admin", form=form)
    # return render_template('00_admin.html', posts = posts)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)


        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your acc has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('00_account.html', title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = News.query.filter_by(author=user).order_by(News.pub_date.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instraction', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid token", 'warning')
        return redirect(url_for('users.reset_request'))
    form = RequestResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your pass has been updated! You can login", 'success')
        return redirect(url_for('users.login'))
    return render_template('00_register.html', title="Login-admin", form=form)
