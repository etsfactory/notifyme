import os
import logging.config
import ast
from utils.config_manager import ConfigManager

APP_NAME = "notifyme"
APP_CHARSET = 'UTF-8'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Config file paths
CONFIGURATION_JSON_FILE = 'config.json'
CONFIGURATION_JOSN_FILE_DEV = 'config_development.json'

config = ConfigManager(CONFIGURATION_JSON_FILE, CONFIGURATION_JOSN_FILE_DEV)

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
DB_USER = config.load('DB_USER', 'db', 'user')
DB_PASSWORD = config.load('DB_PASSWORD', 'db', 'password')

REFRESH_DATABASE = config.load('DB_REFRESH', 'db', 'refresh_database')

API_SERVER = config.load('API_SERVER', 'api', 'server')
API_PORT = config.load('API_PORT', 'api', 'port')

DEFAULT_TEMPLATE_TEXT = config.load('DEFAULT_TEMPLATE_TEXT', 'default_template', 'text')
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
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT_PATH, '{0}/{0}.log'.format(APP_NAME)),
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        'notify_me': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Logger inicialization
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('notify_me')

