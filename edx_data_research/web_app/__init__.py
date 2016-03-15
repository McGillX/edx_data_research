from flask import Flask
from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import MongoEngineUserDatastore, Security

# Create app
app = Flask(__name__)
app.config.from_object('config')

# Create mail object
mail = Mail(app)
