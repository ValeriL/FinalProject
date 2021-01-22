"""Page routes module."""
from datetime import datetime
from typing import List, Tuple

from app import app, db
from app.calculations import (
    get_amount_negative,
    get_amount_positive,
    get_sentiments_percent,
)
from app.error import NoReviews
from app.forms import MovieSearchForm
from app.models import MovieInfo
from app.pdf_creator import create_history_pdf
from app.predictions import get_predictions
from app.scraper import get_all_movies
from flask import redirect, render_template, request, url_for
from sqlalchemy.exc import SQLAlchemyError


@app.route("/", methods=["GET", "POST"])
@app.route("/main", methods=["GET", "POST"])
def main_page() -> str:
    """Get a main page with movie search."""
    form = MovieSearchForm()
    if request.method == "POST":
        title = form.movie_title.data
        movies = get_all_movies(title)
        amount = len(movies)
        if amount == 0:
            return render_template("error.html", error="No movie found.")
        elif amount == 1:
            return redirect(url_for("result", movie=movies[0]))
        else:
            return redirect(url_for("search_results", movies=movies))
    return render_template("main.html", form=form)


@app.route("/result/<tuple:movie>", methods=["GET", "POST"])
def result(movie: Tuple[str, str]) -> str:
    """Get page with review analysis information."""
    correct_title, movie_id = movie
    if db.session.query(db.exists().where(MovieInfo.title == correct_title)).scalar():
        movie = (
            MovieInfo.query.order_by(MovieInfo.movie_id.desc())
            .filter_by(title=correct_title)
            .first()
        )
        if (datetime.today() - movie.search_date).days < 30:
            new_movie = MovieInfo(
                title=correct_title,
                positive_percent=movie.positive_percent,
                negative_percent=movie.negative_percent,
                amount_positive_reviews=movie.amount_positive_reviews,
                amount_negative_reviews=movie.amount_negative_reviews,
            )
    else:
        predictions = get_predictions(movie_id)
        positive_percent, negative_percent = get_sentiments_percent(predictions)
        new_movie = MovieInfo(
            title=correct_title,
            positive_percent=positive_percent,
            negative_percent=negative_percent,
            amount_positive_reviews=get_amount_positive(predictions),
            amount_negative_reviews=get_amount_negative(predictions),
        )
    db.session.add(new_movie)
    db.session.commit()
    create_history_pdf()
    return render_template("result.html", movie=new_movie)


@app.route("/history")
def history() -> str:
    """Get page with search history."""
    movies = MovieInfo.query.order_by(MovieInfo.search_date.desc()).all()
    return render_template("history.html", movies=movies)


@app.route("/search_results/<list:movies>")
def search_results(movies: List[Tuple[str, str]]) -> str:
    """Get page with all founded movies."""
    return render_template("search_results.html", movies=movies)


@app.errorhandler(SQLAlchemyError)
def handle_db_error(error: str) -> str:
    """Get page with db error message."""
    return render_template("error.html", error=error)


@app.errorhandler(NoReviews)
def handle_no_reviews_error(error: str) -> str:
    """Get page with no reviews error message."""
    return render_template("error.html", error=error)
