import json
from app.main import logger
from cryptography.fernet import Fernet

def get_db_info(filename):
    with open (filename) as file_handle:
        data = json.load(file_handle)
    try:
        user = data["user"]
        password = data["password"]
        db = data["db"]
        key = data["cipherkey"]
        logger.debug("Was able to successfully parse the file and "
              "extract the username, password, db-name and key from {0}".format(filename))

    except:
        logger.error("Could not find username, password, db-name and key in the file. "
               "Please check the {0} again".format(filename))
        user = None
        password = None
        db = None
        key = None

    return user, password, db, key


class Config:
    DEBUG = False
    FILENAME = "/etc/blog-it/mongodb-passwd"
    MONGO_USERNAME, MONGO_PASSWORD, MONGO_DBNAME, MONGO_CIPHERKEY = get_db_info(FILENAME)
    MONGO_HOST = "blogit-demo.westus2.cloudapp.azure.com"
    MONGO_PORT = 27018
    MONGO_AUTH_SOURCE = MONGO_DBNAME
    MONGO_URI = "mongodb://{0}:{1}@{2}:{3}/{4}?authSource={5}".format(
        MONGO_USERNAME, MONGO_PASSWORD,
        MONGO_HOST, MONGO_PORT,
        MONGO_DBNAME, MONGO_AUTH_SOURCE
    )




class DevelopmentConfig(Config):

    DEBUG = True
    MONGO_PORT = 27017
    # MONGO_URI = "mongodb://{0}:{1}@{2}:{3}/{4}?authSource={5}".format(
    #     Config.MONGO_USERNAME, Config.MONGO_PASSWORD,
    #     Config.MONGO_HOST, MONGO_PORT,
    #     Config.MONGO_DBNAME, Config.MONGO_AUTH_SOURCE
    # )
    MONGO_URI = "mongodb://{0}:{1}@{2}:{3}/{4}".format(
        Config.MONGO_USERNAME, Config.MONGO_PASSWORD,
        Config.MONGO_HOST, MONGO_PORT, Config.MONGO_DBNAME
    )

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

