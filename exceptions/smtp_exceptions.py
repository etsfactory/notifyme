import errors as e


class SMTPError(Exception):
    def __init__(self, name, msg):
        super(SMTPError, self).__init__(msg)
        e.process_exception(SMTPError, name, msg)


class SMTPAuthenticationError(SMTPError):
    """
    SMTP Auth error
    """

    def __init__(self, msg=None):
        self.name = 'SMTP login error'
        if msg is None:
            msg = "An error occured loggin into the SMTP server"
        super(SMTPAuthenticationError, self).__init__(self.name, msg)


class SMTPSendEmailError(SMTPError):
    """
    SMTP Error sending email
    """

    def __init__(self, msg=None):
        self.name = 'SMTP email send error'
        if msg is None:
            msg = "An error occured sending email to the SMTP server"
        super(SMTPSendEmailError, self).__init__(self.name, msg)
