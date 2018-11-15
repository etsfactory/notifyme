import os
import logging.config
import ast
from utils.config_manager import ConfigManager

APP_NAME = "notifyme"
APP_CHARSET = 'UTF-8'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Config file paths
CONFIGURATION_FILE = 'config.json'
CONFIGURATION_FILE_DEV = 'config_development.json'
CONFIGURATION_FILE = 'config.ini'

config = ConfigManager(CONFIGURATION_FILE, CONFIGURATION_FILE_DEV, CONFIGURATION_FILE)

LOG_ROOT_PATH = config.load('LOG_ROOT_PATH', 'loggin', 'root_path')
RABBITMQ_SERVER = config.load('RABBITMQ_SERVER', 'bus', 'host')
RABBITMQ_USER = config.load('RABBITMQ_USER', 'bus', 'user')
RABBITMQ_PASSWORD = config.load('RABBITMQ_PASSWORD', 'bus', 'password')
RABBITMQ_QUEUE = config.load('RABBITMQ_QUEUE', 'bus', 'queue_name')
RABBIRMQ_EXCHANGE_ERROR = config.load('RABBIRMQ_EXCHANGE_ERROR', 'bus', 'error_exchange')

SMTP_EMAIL = config.load('SMTP_EMAIL', 'smtp', 'email')
SMTP_HOST = config.load('SMTP_HOST', 'smtp', 'server')
SMTP_PORT = config.load('SMTP_PORT', 'smtp', 'port')
SMTP_PASS = config.load('SMTP_PASS', 'smtp', 'password')

DB_SERVER = config.load('DB_SERVER', 'db', 'server')
DB_PORT = config.load('DB_SERVER', 'db', 'port')
REFRESH_DATABASE = config.load('DB_REFRESH', 'db', 'refresh_database')

DEFAULT_TEMPLATE_TEXT = config.load('DEFAULT_TEMPLATE_TEXT', 'default_template', 'text')
print(DEFAULT_TEMPLATE_TEXT)
DEFAULT_TEMPLATE_SUBJECT = config.load('DEFAULT_TEMPLATE_SUBJECT', 'default_template', 'subject')

DB_NAME = 'notify_me'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "%(asctime)s.%(msecs)04d %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)-7s:  %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'notify_me': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Logger inicialization
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('notify_me')

