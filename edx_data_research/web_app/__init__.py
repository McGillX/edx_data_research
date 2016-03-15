from flask import Flask
from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import MongoEngineUserDatastore, Security

# Create app
app = Flask(__name__)
app.config.from_object('config')

# Create mail object
mail = Mail(app)

# Create database connection object
db = MongoEngine(app)

from edx_data_research.web_app.models import User, Role

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)
