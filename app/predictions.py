"""Module for making predictions via reviews and loaded model."""
import pickle  # noqa: S403
import re
import string
from typing import List

import numpy as np
from app.scraper import get_all_reviews
from nltk import WhitespaceTokenizer, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords, wordnet


def get_predictions(movie_id: str) -> np.ndarray:
    """Get all reviews and return predictions for all."""
    reviews = get_all_reviews(movie_id)
    return predict_sentiments(reviews)


def predict_sentiments(reviews: List[str]) -> np.ndarray:
    """Predict a sentiment for input reviews."""
    vectorizer = pickle.load(open("training/vectorizer.pickle", "rb"))  # noqa: S301
    model = pickle.load(open("training/sentiment_model.sav", "rb"))  # noqa: S301
    vectorized_reviews = vectorizer.transform(
        clean_review(review) for review in reviews
    ).toarray()
    return model.predict(vectorized_reviews)


def clean_review(review: str) -> str:
    """Clean a review of unnecessary symbols."""
    stop_words = set(stopwords.words("english"))
    tokenizer = WhitespaceTokenizer()
    lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(word: str) -> str:
        """Get wordnet pos (part of speech) tags."""
        word_and_tag = pos_tag([word])[0]
        tag = word_and_tag[1]
        short_tag = tag[0]
        tag_dict = {
            "J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV,
        }
        return tag_dict.get(short_tag, wordnet.NOUN)

    review = re.sub("<.*?>", " ", review)
    review = review.translate(
        str.maketrans(string.punctuation + string.digits, 42 * " ")
    )
    review_tokens = tokenizer.tokenize(review)
    lower_review_tokens = (token.lower() for token in review_tokens)
    review_tokens = (token for token in lower_review_tokens if token not in stop_words)
    review_lemmas = (
        lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in review_tokens
    )
    return " ".join(review_lemmas)
