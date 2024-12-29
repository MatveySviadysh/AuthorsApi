import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
error_handler = RotatingFileHandler(
    'logs/error.log',
    maxBytes=10485760,
    backupCount=5
)
access_handler = RotatingFileHandler(
    'logs/access.log',
    maxBytes=10485760,
    backupCount=5
)

app_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
access_handler.setFormatter(formatter)

app_logger = logging.getLogger('app')
app_logger.setLevel(logging.INFO)
app_logger.addHandler(app_handler)

error_logger = logging.getLogger('error')
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)

access_logger = logging.getLogger('access')
access_logger.setLevel(logging.INFO)
access_logger.addHandler(access_handler) 