from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SummonerSearchForm(FlaskForm):
    summoner = StringField('Summoner', validators=[DataRequired(), Length(min=3, max=24)])
    submit = SubmitField('Search')
