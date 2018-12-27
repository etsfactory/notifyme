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
        except:  # smtplib.SMTPServerDisconnected
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
        self.server.starttls()
        
        if not self.is_connected():
            self.login()

        try:
            msg = email.message.Message()
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = ", ".join(send_to)
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(body)
            self.server.sendmail(
                msg['From'], send_to, msg.as_string().encode('utf-8'))
            self.server.quit()
        except BaseException:
            raise SMTPSendEmailError()
