from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    number = IntegerField('number', validators=[DataRequired()])
    from_number = IntegerField('from_number')
    to_number = IntegerField('to_number')
    attempts = IntegerField('attempts')
    id = IntegerField('id')
