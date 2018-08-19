from flask import Blueprint, jsonify, request
from app.main import logger, get_collection_map, mongo, pymongo
from bson.json_util import loads,dumps
import json
from app.main.collection_lib import CollectionClass
articles_mod = Blueprint('articles', __name__)
from flask_cors import CORS
from bson.objectid import ObjectId

CORS(articles_mod, resources={r"/*": {"origins": "*"}})

def user_exit(collection_name=None, user=None):
    user_exit = True

    cursor = CollectionClass(mongo.db[collection_name]).\
        find_one(filter={'username' : user})

    if cursor is None:
        logger.error('Username "{0}" does not exist.'.format(user))
        user_exit = False
    return user_exit

@articles_mod.route('/articles', methods=['GET'])
def get_articles():
    """
    /articles?username=kmanek&limit=2
        Get all articles owned by kmanek where limit is 2 (This is for the first page)
        
    /articles?username=kmanek&id=5b664e9bd09275c1286c86a1&limit=2
        Get all articles owned by kmanek where id > 5b664e9bd09275c1286c86a1 and limit is 2 (this is for all pages except first)
        
    /articles?limit=2
        Get all articles from all owners where limit is 2 (This is for the first page)
            
    /articles?id=5b664e9bd09275c1286c86a1&limit=2
        Get all articles from all owners where id > 5b664e9bd09275c1286c86a1 and limit is 2 (this is for all pages except first)
        
    /articles
        This is not yet defined and will throw user does not exist error
     
    """
    logger.debug('Welcome to get all articles page')

    # Parse the request arguments
    article_collection = get_collection_map('article')
    user_collection = get_collection_map('user')

    # parse username, default is None
    username = request.args.get('username', default=None)

    # default value of limit is 10 is not specified
    limit = int(request.args.get('limit', default="10"))

    # default value of last_id will be 0 for the first page
    last_id_rcvd = request.args.get('last_id', default="000000000000000000000000")

    logger.debug("Received GET request for the foll parameters {0}".format(request.args))

    # If username is provided and exist then return all articles owned by that username.
    # If username is provided and does not exist then return with error.
    if username:
        if user_exit(collection_name=user_collection, user=username):
            search_filter = {'article_owner_id': username,
                                 "_id": {"$gt": ObjectId(last_id_rcvd)}}
        else:
            return jsonify(message='Username \'{0}\' does not exist.'.format(username)), 400

    # If username is not provided then return all articles.
    else:
        search_filter = {"_id": {"$gt": ObjectId(last_id_rcvd)}}


    article_obj = CollectionClass(mongo.db[article_collection]). \
                find(filter=search_filter, limit=limit, sort=[("_id",pymongo.DESCENDING)])

    # Convert pymongo cursor to list, so that it can be converted to JSON later on
    article_data = list(article_obj)

    try:
        object_id_str = dumps(article_data[0]["_id"])
        object_id_json = json.loads(object_id_str)
        last_id_sent = object_id_json["$oid"]
    # this will trigger when there are no more articles to be shown, hence make last_id_sent = -1
    except IndexError as e:
        logger.exception(e)
        last_id_sent = -1

    # TODO: Ask Gareth if he wants 204 status code with no content or send empty JSON with 200 status code

    return jsonify(message=dumps(article_obj),
                       last_id=last_id_sent), 200

