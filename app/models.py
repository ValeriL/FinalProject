"""SQLAlchemy table models."""
from datetime import datetime

from app import db


class MovieInfo(db.Model):
    """Table model for movie's information."""

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    positive_percent = db.Column(db.Integer)
    negative_percent = db.Column(db.Integer)
    amount_positive_reviews = db.Column(db.Integer)
    amount_negative_reviews = db.Column(db.Integer)
    search_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Instance representation."""
        return "<Movie {}: +{}%>".format(self.title, self.positive_percent)
