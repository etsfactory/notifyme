"""
SMTP Handler
"""
import smtplib
import email.message
import settings as st

from exceptions.smtp_exceptions import SMTPAuthenticationError, SMTPSendEmailError

class SMTPHandler(object):
    """
    SMTPHandler class to send emails
    """
    def __init__(self, username, password, host, port):
        """
        Initializes the connection with SMTP server provided and login with username and password
        """
        self.username = username
        self.passwod = password
        self.host = host
        self.port = port
        try:
            self.server = smtplib.SMTP_SSL(host, port)
            self.server.ehlo()
            self.server.login(username, password)
        except:
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
            msg.add_header('Content-Type','text/html')
            msg.set_payload(body)
            self.server.sendmail(msg['From'], [msg['To']], msg.as_string())
        except:
            raise SMTPSendEmailError()