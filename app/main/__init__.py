from flask import Flask
from flask_pymongo import PyMongo

from config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    mongo = PyMongo(app)
    # print mongo
    # print dir(app.config), app.config.keys(), dir (mongo.db)
    # dir(mongo.db)
    # print list(mongo.db["demo_collections"].find())
    # try:
    #     print mongo.db.collection_names()
    #
    # except Exception as e:
    #     print "Could not connect to MongoDB: {0}".format(e)
    #     return None, None

    return app, mongo

create_app("dev")