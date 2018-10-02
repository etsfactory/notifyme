import smtplib
class SMTPHandler:

    username = ''
    password = 'Frost45200'
    host = ''
    port = ''
    server = None

    def __init__(self, username, password, host, port):
        self.username = username
        self.passwod = password
        self.host = host
        self.port = port
        try:
            self.server = smtplib.SMTP_SSL(host, port)
            self.server.ehlo()
            self.server.login(username, password)
        except:
            print 'Error login with username: ', username, 'and password: ', password

    def send_email(self, sent_from, sent_to, email_text):
        try:
            self.server.sendmail(sent_from, sent_to, email_text)
            self.server.close()
            print 'Email sent to ', sent_to
        except:
            print 'Error sending email'
