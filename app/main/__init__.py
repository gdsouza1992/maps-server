from flask import Flask
from flask_pymongo import PyMongo, pymongo

import logging
import os

class LogCreate():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Get the root directory aka base_dir
        base_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")

        # Create the Handler for logging data to a file
        logger_handler = logging.FileHandler('{0}/logs/python_logging.log'.format(base_dir))
        logger_handler.setLevel(logging.DEBUG)

        # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(module)s: %(message)s')
        logger_handler.setFormatter(logger_formatter)

        # Add the Handler to the Logger
        self.logger.addHandler(logger_handler)
        # logger.info('Completed configuring logger()!')

    def get_logger(self):
        return self.logger


log = LogCreate()
logger = log.get_logger()
logger.debug("Successfully completed the logging configurations")

collection_map = {
    "article": "demo-article",
    "place": "demo-place",
    "user": "demo-user"
}

from .config import config_by_name
# def create_app(config_name):
app = Flask(__name__)
app.config.from_object(config_by_name['dev'])
mongo = PyMongo(app)


def get_collection_map(key):
    return collection_map[key]

# create_app("dev")
# create_logger()
