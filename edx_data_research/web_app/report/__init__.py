from flask import Blueprint

report = Blueprint('report', __name__, url_prefix='/report')

from . import views