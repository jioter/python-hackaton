from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class GamePlayForm(FlaskForm):
    number = IntegerField('number', validators=[DataRequired()])
