from flask import Blueprint

parse = Blueprint('parse', __name__, url_prefix='/parse')

from . import views