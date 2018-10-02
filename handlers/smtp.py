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

    def send_email(self, sent_to, subject, email_text):
        """
        Send temail trough SMTP from account to a list of emails (sent_to) with a message
        """
        try:
            message = 'Subject: {}\n\n{}'.format(subject, email_text)
            self.server.sendmail(self.username, sent_to, message)
            self.server.close()
            print 'Email sent to ', sent_to
        except SMTPSendEmailError:
            print 'Error sending email'
