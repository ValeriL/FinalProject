"""Page routes module."""
from typing import List, Tuple

from app import app, db
from app.calculations import (
    get_amount_negative,
    get_amount_positive,
    get_negative_percent,
    get_positive_percent,
)
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
            return redirect(url_for("error_handler", erorr="No movie found."))
        elif amount == 1:
            return redirect(url_for("result", movie=movies[0]))
        else:
            return redirect(url_for("search_results", movies=movies))
    return render_template("main.html", form=form)


@app.route("/result/<tuple:movie>", methods=["GET", "POST"])
def result(movie: Tuple[str, str]) -> str:
    """Get page with review analysis information."""
    correct_title, movie_id = movie
    try:
        predictions = get_predictions(movie_id)
    except Exception:
        return redirect(url_for("error_handler", error="No reviews yet."))
    movie = MovieInfo(
        title=correct_title,
        positive_percent=get_positive_percent(predictions),
        negative_percent=get_negative_percent(predictions),
        amount_positive_reviews=get_amount_positive(predictions),
        amount_negative_reviews=get_amount_negative(predictions),
    )
    try:
        db.session.add(movie)
        db.session.commit()
    except SQLAlchemyError:
        error = "Database error."
        return redirect(url_for("error_handler", error=error))
    create_history_pdf()
    return render_template("result.html", movie=movie)


@app.route("/history")
def history() -> str:
    """Get page with search history."""
    movies = MovieInfo.query.order_by(MovieInfo.search_date.desc()).all()
    return render_template("history.html", movies=movies)


@app.route("/search_results/<list:movies>")
def search_results(movies: List[Tuple[str, str]]) -> str:
    """Get page with all founded movies."""
    return render_template("search_results.html", movies=movies)


@app.route("/error/<error>")
def error_handler(error: str) -> str:
    """Get page with error message."""
    return render_template("error.html", error=error)
