"""Module with error class."""


class NoReviews(Exception):
    """Exception class for no revews error."""

    def __init__(self, text: str):
        self.text = text
