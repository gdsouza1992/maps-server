import os
import json


basedir = os.path.abspath(os.path.dirname(__file__))

def get_db_info(filename):
    with open (filename) as file_handle:
        data = json.load(file_handle)
    try:
        user = data["user"]
        password = data["password"]
        db = data["db"]

        print "Was able to successfully parse the file and " \
              "extract the username, password and db-name"

    except:
        print "Could not find username, password and db-name in the file. " \
               "Please check the {0} again".format(filename)
        user = None
        password = None
        db = None

    return user, password, db


class Config:
    # SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    FILENAME = "/etc/blog-it/mongodb-passwd"
    MONGO_USERNAME, MONGO_PASSWORD, MONGO_DBNAME = get_db_info(FILENAME)
    MONGO_HOST = "blogit-demo.westus2.cloudapp.azure.com"
    MONGO_PORT = 27018
    MONGO_AUTH_SOURCE = MONGO_DBNAME
    MONGO_URI = "mongodb://{0}:{1}@{2}:{3}/{4}?authSource={5}".format(
        MONGO_USERNAME, MONGO_PASSWORD,
        MONGO_HOST, MONGO_PORT,
        MONGO_DBNAME, MONGO_AUTH_SOURCE
    )




class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base

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
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    # PRESERVE_CONTEXT_ON_EXCEPTION = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

# key = Config.SECRET_KEY