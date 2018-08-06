from flask import Blueprint, jsonify, request
from app.main import logger, get_collection_map, mongo, pymongo
import json
from bson.json_util import loads,dumps
from app.main.collection_lib import CollectionClass
articles_mod = Blueprint('articles', __name__)
from flask_cors import CORS

CORS(articles_mod, resources={r"/*": {"origins": "*"}})


@articles_mod.route('/articles', methods=['GET'])
def get_articles():
    logger.debug('Welcome to get all articles page')

    # Parse the request arguments
    article_collection = get_collection_map('article')
    user_collection = get_collection_map('user')

    username = request.args.get('username')
    user_obj = CollectionClass(mongo.db[user_collection]).find_one({'username' : username})
    if user_obj is None:
        logger.error('Username: {0} does not exist.'.format(user_obj))
        return jsonify(message='Username: {0} does not exist.'.format(user_obj)), 400
    else:
        article_obj = CollectionClass(mongo.db[article_collection]).find({'article_owner_id' : username})
        return dumps(article_obj), 200
