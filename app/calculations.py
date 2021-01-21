"""Calculations module for given sentiment predictions array."""
from typing import List


def get_amount_positive(predictions: List[bool]) -> int:
    """Get amount of positive reviews."""
    return int((predictions == 1).sum())


def get_amount_negative(predictions: List[bool]) -> int:
    """Get amount of negative reviews."""
    return int((predictions == 0).sum())


def get_positive_percent(predictions: List[bool]) -> int:
    """Get a percent of positive reviews."""
    return round(get_amount_positive(predictions) / len(predictions) * 100)


def get_negative_percent(predictions: List[bool]) -> int:
    """Get a percent of negative reviews."""
    return 100 - get_positive_percent(predictions)
