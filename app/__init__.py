from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .utils import ListConverter, TupleConverter


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.url_map.converters["list"] = ListConverter
app.url_map.converters["tuple"] = TupleConverter

from app import models, routes  # noqa: E402, I100
