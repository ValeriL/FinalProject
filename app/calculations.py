"""Calculations module for given sentiment predictions array."""
from typing import Tuple

import numpy as np


def get_amount_positive(predictions: np.ndarray) -> int:
    """Get amount of positive and negative reviews."""
    return int((predictions == 1).sum())


def get_amount_negative(predictions: np.ndarray) -> int:
    """Get amount of negative reviews."""
    return int((predictions == 0).sum())


def get_sentiments_percent(predictions: np.ndarray) -> Tuple[int, int]:
    """Get a percent of positive and negative reviews."""
    positive = round(get_amount_positive(predictions) / len(predictions) * 100)
    negative = 100 - positive
    return positive, negative
