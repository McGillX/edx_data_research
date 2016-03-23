from flask import Blueprint

parse = Blueprint('parse', __name__)

from . import views
