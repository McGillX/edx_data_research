from flask_security.forms import RegisterForm
from wtforms import Required

class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [Required(message='Username not provided')])