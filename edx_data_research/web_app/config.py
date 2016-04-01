import os


WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('MCGILLX_SECRET_KEY') or 'you-will-never-guess'

# Flask-Mail configuration
MAIL_SERVER = 'smtp.mcgill.ca'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MCGILLX_MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MCGILLX_MAIL_PASSWORD')

# Flas-Security Configuration
SECURITY_BLUEPRINT_NAME = 'auth'
SECURITY_CHANGEABLE = True
SECURITY_EMAIL_SENDER = 'McGillX Team <{0}>'.format(os.environ.get('MCGILLX_MAIL_USERNAME'))
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = os.environ.get('MCGILLX_PASSWORD_SALT')
SECURITY_POST_LOGIN_VIEW = '/home'
SECURITY_RECOVERABLE = True
SECURITY_REGISTERABLE = True
SECURITY_URL_PREFIX = '/auth'
