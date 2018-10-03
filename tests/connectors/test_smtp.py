import pytest
from notify_me.connectors.smtp import SMTPHandler

def test_smtp_login():
    print 'The SMTP Handler raises exception if the user and the password are wrong'
    with pytest.raises(Exception):
        smtp = SMTPHandler('dlopez@ets.es', '12345', 'smtp.gmail.com', 465)
