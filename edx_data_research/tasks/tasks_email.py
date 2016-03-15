import os
import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from edx_data_research.tasks.tasks import Tasks


class Email(Tasks):

    def __init__(self, args):
        super(Email, self).__init__()
        self.from_address = args.from_address
        self.from_name = args.from_name
        self.password = args.password
        self.body = args.body
        self.to_address = args.to_address
        self.subject = args.subject
        self.attachments = args.attachments

    def do(self):
        message = self.init_email()
        if self.body:
            message.attach(self.body)
        for attachment in self.attachments:
            message.attach(self.upload_attachment(attachment))
        self.send_email(message)

    def init_email(self):
        message = MIMEMultipart()
        message['From'] = self.from_name or self.from_address
        message['To'] = ','.join(self.to_address)
        message['Subject'] = self.subject
        return message

    @staticmethod
    def file_name(file_path):
        _, tail = os.path.split(file_path)
        return tail

    def upload_attachment(self, attachment):
        name = Email.file_name(attachment)
        with open(attachment, 'rb') as fp:
            file_attachment = MIMEText(fp.read())
            file_attachment.add_header('Content-Disposition', 'attachment',
                                        filename=name)
        return file_attachment

    def compose_email(self):
        self.message = self.init_email()
        for attachment in self.attachments:
            self.message.attach(self.upload_attachment(attachment))
        return self.message

    def send_email(self, composed_email):
        server = smtplib.SMTP('smtp.mcgill.ca', 587)
        server.starttls()
        server.login(self.from_address, self.password)
        server.sendmail(self.from_address, self.to_address,
                        composed_email.as_string())
