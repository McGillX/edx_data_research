from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security


db = MongoEngine()
mail = Mail()
security = Security()