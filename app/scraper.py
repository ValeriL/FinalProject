"""Page scrapers module."""
from typing import List, Tuple

import requests


def get_all_movies(name: str) -> Tuple[str, str]:  # noqa: CCR001: 7 > 5
    """Get movie id and its correct name via given movie name request."""
    url = "https://google-search5.p.rapidapi.com/google-serps/"
    querystring = {"q": f"{name} imdb", "pages": "1", "gl": "us", "autocorrect": "1"}
    headers = {
        "x-rapidapi-key": "1943403269mshd455dfb5beafc5ep1797f6jsn5395f994d5c1",
        "x-rapidapi-host": "google-search5.p.rapidapi.com",
    }
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    movie_results = response["data"]["results"]["organic"]
    movie_info = []
    movies = set()
    for movie in movie_results:
        movie_url = movie["url"]
        if movie_url.startswith("https://www.imdb.com/title/") and movie_url.endswith(
            "/"
        ):
            movie_id = movie_url.split("/")[-2]
            movie_title = movie["title"][:-7]
            if movie_title not in movies:
                movies.add(movie_title)
                movie_info.append((movie_title, movie_id))
    return movie_info


def get_all_reviews(movie_id: str) -> List[str]:
    """Get all reviews from IMDB site via movie id."""
    reviews = []
    pagination_key = None
    for _ in range(5):
        pagination_key, page_reviews = get_page_reviews(movie_id, pagination_key)
        reviews.extend(page_reviews)
        if not pagination_key:
            break
    if not reviews:
        raise Exception
    return reviews


def get_page_reviews(movie_id: str, pagination_key: str = None) -> Tuple[str, str]:
    """Get reviews from one page and pagination key for the next page."""
    url = "https://imdb8.p.rapidapi.com/title/get-user-reviews"
    querystring = {"tconst": movie_id, "paginationKey": pagination_key}
    headers = {
        "x-rapidapi-key": "1943403269mshd455dfb5beafc5ep1797f6jsn5395f994d5c1",
        "x-rapidapi-host": "imdb8.p.rapidapi.com",
    }
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    try:
        pagination_key = response["paginationKey"]
    except KeyError:
        pagination_key = None
    try:
        reviews = [
            f"{review['reviewTitle']} {review['reviewText']}"
            for review in response["reviews"]
        ]
    except KeyError:
        reviews = []
    return pagination_key, reviews
