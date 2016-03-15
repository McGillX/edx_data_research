import os


WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('MCGILLX_SECRET_KEY') or 'you-will-never-guess'
MAIL_SERVER = 'smtp.mcgill.ca'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MCGILLX_MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MCGILLX_MAIL_PASSWORD')
