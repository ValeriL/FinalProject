"""Page routes module."""
from app import app
from app.forms import MovieSearchForm
from app.models import MovieInfo
from flask import redirect, render_template, url_for


@app.route("/", methods=["GET", "POST"])
@app.route("/main", methods=["GET", "POST"])
def main_page() -> str:
    """Get a main page with movie search."""
    form = MovieSearchForm()
    if form.validate_on_submit():
        return redirect(url_for("result"))
    return render_template("main.html", form=form)


@app.route("/result", methods=["GET", "POST"])
def result() -> str:
    """Get page with review analysis information."""
    movie = {"name": "Game of Thrones", "pos_per": 80, "neg_per": 20}
    return render_template("result.html", movie=movie)


@app.route("/history")
def history() -> str:
    """Get page with search history."""
    bd_data = MovieInfo.query.all()
    return render_template("history.html", bd_data=bd_data)
