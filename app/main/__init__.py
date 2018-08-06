from flask import Flask
from flask_pymongo import PyMongo, pymongo

#from .config import config_by_name,Config
from cryptography.fernet import Fernet
import logging
import os
import errno

class LogCreate():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Get the root directory aka base_dir
        base_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")
        self.mkdir("{0}/logs".format(base_dir))

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

    def mkdir(self, base_dir):
        try:
            os.makedirs(base_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                self.logger.error("unable to create {0} directory due to the following error {1}".format(base_dir, e))


log = LogCreate()
logger = log.get_logger()
logger.debug("Successfully completed the logging configurations")

collection_map = {
    "article": "demo-articles",
    "place": "demo-place",
    "user": "demo-user"
}
from .config import config_by_name,Config
cipher_obj = Fernet(Config.MONGO_CIPHERKEY)
# def create_app(config_name):
app = Flask(__name__)
app.config.from_object(config_by_name['dev'])
mongo = PyMongo(app)


def get_collection_map(key):
    return collection_map[key]

# create_app("dev")
# create_logger()
