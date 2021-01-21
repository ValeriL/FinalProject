"""SQLAlchemy table models."""
from datetime import datetime

from app import db


class MovieInfo(db.Model):
    """Table model for movie's information."""

    name = db.Column(db.String(64), index=True)
    pos_per = db.Column(db.Integer)
    neg_per = db.Column(db.Integer)
    amount_pos_reviews = db.Column(db.Integer)
    amount_neg_reviews = db.Column(db.Integer)
    search_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Instance representation."""
        return "<Movie {}: +{}% -{}%>".format(self.username, self.pos_per, self.neg_per)
