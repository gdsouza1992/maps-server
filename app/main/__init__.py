from flask import Flask
from flask_pymongo import PyMongo
from .config import config_by_name
import logging



def create_logger():
    # Create the Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create the Handler for logging data to a file
    logger_handler = logging.FileHandler('logs/python_logging.log')
    # logger_handler.setLevel(logging.DEBUG)

    # Create a Formatter for formatting the log messages
    logger_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')
    logger_handler.setFormatter(logger_formatter)

    # Add the Handler to the Logger
    logger.addHandler(logger_handler)
    logger.info('Completed configuring logger()!')

    return logger

collection_map = {
    "article":"demo-article",
    "place":"demo-place",
    "user":"demo-user"
}

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    mongo = PyMongo(app)
    return app, mongo

def get_collection_map(key):
    return collection_map[key]

# create_app("dev")