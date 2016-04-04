from flask_bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security


bootstrap = Bootstrap()
db = MongoEngine()
mail = Mail()
security = Security()
