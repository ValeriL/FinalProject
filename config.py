"""Configuration options module."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "I-have-no-bloody-idea"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "example.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
