"""Flask forms module."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class MovieSearchForm(FlaskForm):
    """Form for movie search on the main page."""

    movie_name = StringField(
        "Enter the movie name:", validators=[InputRequired("No movie name entered")]
    )
    submit = SubmitField("Submit")
