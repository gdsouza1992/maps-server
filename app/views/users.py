from flask import Blueprint, jsonify, request
from app.main import logger, get_collection_map, mongo
import json
from app.main.collection_lib import CollectionClass
user_mod = Blueprint('user', __name__)


#####################################################################################################
# Signup Post Routine : returns username,password with code=200 if new user
#                      else returns Username Taken msg with code=400
#####################################################################################################
@user_mod.route('/signup', methods=['POST'])
def signup():
    logger.debug('Welcome to SIGN UP page')
    collection = get_collection_map('user')
    # print collection
    json_data = json.loads(request.data)
    username = json_data.get('username')
    email_id = json_data.get('email')
    # password = json_data.get('password')
    # return jsonify(status="Bad"), 500
    if CollectionClass(mongo.db[collection]).find_one({'username': username}) is None:
        if CollectionClass(mongo.db[collection]).insert_many([json_data]):
            return jsonify(username=username, email=email_id), 200
        else:
            return jsonify(status="Bad"), 500
    else:
        logger.info('Username already taken, please choose another one')
        return jsonify(message="Username already taken, please choose another one"), 400


#####################################################################################################
# Signin Post Routine : returns Valid user with code=200 if username/email and password matches
#                      else returns Invalid username/password with code=400
#####################################################################################################
@user_mod.route('/signin', methods=['POST'])
def signin():
    logger.debug('Welcome to SIGN IN page')
    collection = get_collection_map('user')
    # print collection
    json_data = json.loads(request.data)
    username = json_data.get('username')
    # email_id = json_data.get('email')
    # password = json_data.get('password')
    # return jsonify(status="Bad"), 500
    obj = CollectionClass(mongo.db[collection]).find_one({'$or': [{'username': username}, {'email': username}]})
    if obj is not None:
        if json_data.get('password') == obj['password']:
            logger.info('User Credentials Authentication Successful')
            return jsonify(message="User Credentials Authentication Successful"), 200
        else:
            logger.warning('Wrong Password')
            return jsonify(message="Invalid Username or Password"), 400
    else:
        logger.info('Invalid Username')
        return jsonify(message="Invalid Username or Password"), 400
