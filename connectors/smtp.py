"""
SMTP Handler
"""
import smtplib

class SMTPAuthenticationError(Exception):
    """
    SMTP Auth error
    """

class SMTPSendEmailError(Exception):
    """
    SMTP Error sending email
    """

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
        except SMTPAuthenticationError:
            print 'Error login with username: ', username, 'and password: ', password

    def send_email(self, send_to, subject, body):
        """
        Send temail trough SMTP from account to a list of emails with a message
        :send_to: List of emails to send email
        :subject: The subject of the email
        :body: The body of the email
        """
        try:
            message = 'Subject: {}\n\n{}'.format(subject, body)
            self.server.sendmail(self.username, send_to, message)
            print 'Email sent to ', send_to
        except SMTPSendEmailError:
            print 'Error sending email'
