from threading import Thread

from flask import render_template
from flask.ext.mail import Message

from edx_data_research.web_app import app, mail

MAIL_SENDER = 'McGillX Team <{0}>'.format(app.config['MAIL_USERNAME'])


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender=MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr