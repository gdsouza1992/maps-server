from flask import Blueprint, jsonify, request
from app.main import logger, get_collection_map, mongo
import json
from app.main.collection_lib import CollectionClass
user_mod = Blueprint('user', __name__)
from flask_cors import CORS

CORS(user_mod, resources={r"/*": {"origins": "*"}})


#####################################################################################################
# Signup Post Routine : returns username,password with code=200 if new user
#                      else returns Username Taken msg with code=400
#####################################################################################################
@user_mod.route('/signup', methods=['POST'])
def signup():
    logger.debug('Welcome to SIGN UP page')

    # Parse the request arguments
    collection = get_collection_map('user')
    json_data = json.loads(request.data)
    username = json_data.get('username', None)
    email_id = json_data.get('email', None)
    password = json_data.get('password', None)

    # Check if the arguments supplied are correct. Also check the contents of the arguments
    if username is "" or password is "" or email_id is "":
        logger.debug("Either Username or Email-ID or Password is NULL")
        logger.debug("Username: {0}, Email-ID: {1}, Password: {2}".format(username, email_id, password))
        return jsonify(message="Either Username or Email-ID or Password is NULL"), 400

    if username is None or password is None or email_id is None:
        logger.debug("Username or Email-ID or Password keyword is incorrect")
        logger.debug("Expected: username/email/password  Got: {0}".format(json_data.keys()))
        return jsonify(message="Expected: username/email/password  Got: {0}".format(json_data.keys())), 400

    if (len(json_data.keys()) != 3):
        logger.debug("Expected: username/email/password  Got: {0}".format(json_data.keys()))
        return jsonify(message="Incorrect number of keys. Expected: username/email/password  Got: {0}".format(json_data.keys())), 400

    # Query the DB for appropriate keyword and return accordingly
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

    # Parse the request arguments
    collection = get_collection_map('user')
    json_data = json.loads(request.data)
    user = json_data.get('username', None)
    password = json_data.get('password', None)

    # Check if the arguments supplied are correct. Also check the contents of the arguments
    if user is "" or password is "":
        logger.debug("Either User/Email or Password is None")
        logger.debug("User/Email: {0}, Password: {1}".format(user, password))
        return jsonify(message="Either User/Email or Password is NULL"), 400

    if user is None or password is None:
        logger.debug("Username or Password keyword is incorrect")
        logger.debug("Expected: username/password  Got: {0}".format(json_data.keys()))
        return jsonify(message="Expected: username/password  Got: {0}".format(json_data.keys())), 400

    # Query the DB for appropriate keyword and return accordingly
    db_obj = CollectionClass(mongo.db[collection]).find_one({'$or': [{'username': user}, {'email': user}]})
    if db_obj is not None:
        if json_data.get('password') == db_obj['password']:
            logger.info('User Credentials Authentication Successful')
            return jsonify(message="User Credentials Authentication Successful"), 200
        else:
            logger.warning('Wrong Password')
            return jsonify(message="Invalid Username or Password"), 400
    else:
        logger.info('Invalid Username')
        return jsonify(message="Invalid Username or Password"), 400
