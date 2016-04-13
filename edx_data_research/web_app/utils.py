import contextlib
import datetime
import os
import shutil
import tempfile

from .args import SendEmail
from edx_data_research import tasks


@contextlib.contextmanager
def temp_dir_context():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


def send_email(to_address, subject, attachments=None):
    from_address = os.environ['FROM_EMAIL_ADDRESS']
    password = os.environ['FROM_EMAIL_PASSWORD']
    to_address = [to_address]
    if attachments is None:
        attachments = []
    args = SendEmail(from_address, None, password, to_address, None,
                     subject, attachments)
    email = tasks.Email(args)
    email.do()
