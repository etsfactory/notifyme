"""
SMTP Handler
"""
import smtplib
import email.message

from exceptions.smtp_exceptions import (
    SMTPAuthenticationError,
    SMTPSendEmailError
)


class SMTPHandler():
    """
    SMTPHandler class to send emails
    """

    def __init__(self, username, password, host, port):
        """
        Initializes the connection with SMTP server and credentials provided
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.server = smtplib.SMTP(host, port)
        self.server.ehlo()
        self.login()

    def login(self):
        """
        Login into smtp server
        """
        if (self.username and self.password):
            try:
                self.server.login(self.username, self.password)
            except BaseException:
                raise SMTPAuthenticationError()

    def send(self, send_to, subject, body):
        """
        Send temail trough SMTP from account to a list of emails with a message
        :send_to: List of emails to send email
        :subject: The subject of the email
        :body: The body of the email. HTML supported
        """
        try:
            msg = email.message.Message()
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = send_to
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(body)
            self.server.sendmail(msg['From'], [msg['To']], msg.as_string())
        except BaseException:
            raise SMTPSendEmailError()
