"""
SMTP Handler
"""
import smtplib
import email.message

from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from exceptions.smtp_exceptions import (
    SMTPAuthenticationError,
    SMTPSendEmailError
)


class SMTPHandler():
    """
    SMTPHandler class to send emails
    """

    def __init__(self, username, password, host, port, from_name, ttls):
        """
        Initializes the connection with SMTP server and credentials provided
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.from_name = from_name
        self.ttls = ttls

    def login(self):
        """
        Login into smtp server
        """
        if (self.username and self.password):
            try:
                self.server.login(self.username, self.password)
            except BaseException:
                raise SMTPAuthenticationError()

    def is_connected(self):
        try:
            status = self.server.noop()[0]
        except BaseException:  # smtplib.SMTPServerDisconnected
            status = -1
        return True if status == 250 else False

    def send(self, send_to, subject, body):
        """
        Send temail trough SMTP from account to a list of emails with a message
        :send_to: List of emails to send email
        :subject: The subject of the email
        :body: The body of the email. HTML supported
        """
        self.server = smtplib.SMTP(self.host, self.port)
        # self.server.set_debuglevel(1)
        self.server.ehlo()
        if self.ttls:
            self.server.starttls()

        if not self.is_connected():
            self.login()

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            author = formataddr((str(Header(self.from_name, 'utf-8')), self.username))
            msg['From'] = author
            part = MIMEText(body, 'html')
            msg.attach(part)
            self.server.sendmail(
                msg['From'], send_to, msg.as_string().encode('utf-8'))
            self.server.quit()

        except BaseException:
            raise SMTPSendEmailError()
