from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User





class RegistrationForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired(), Length(min=2, max=2000)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError("This username is taken.")
    #
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError("This email is taken.")


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('LogIn')


#
# class UpdateAccountForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired(), Length(min=2, max = 20)])
#     email = StringField("Email", validators=[DataRequired(), Email()])
#     # picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
#     submit = SubmitField('Update')
#
#     def validate_username(self, username):
#         if username.data != current_user.username:
#             user = User.query.filter_by(username=username.data).first()
#             if user:
#                 raise ValidationError("This username is taken.")
#
#     def validate_email(self, email):
#         if email.data != current_user.email:
#             user = User.query.filter_by(email=email.data).first()
#             if user:
#                 raise ValidationError("This email is taken.")

# class RequestResetForm(FlaskForm):
#     email = StringField("Email", validators=[DataRequired(), Email()])
#     submit = SubmitField('Request Password Reset')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is None:
#             raise ValidationError("There is no account with those email.")
#
# class ResetPasswordForm(FlaskForm):
#     password = PasswordField("Password", validators=[DataRequired()])
#     confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Reset Password')