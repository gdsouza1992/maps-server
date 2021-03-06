from flask import Blueprint, jsonify, request
from app.main import logger, get_collection_map, mongo, cipher_obj, pymongo
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
    json_data["password"] = cipher_obj.encrypt(bytes(password,'utf-8'))

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
    try:
        CollectionClass(mongo.db[collection]).insert([json_data])
        logger.info("Successfully added {0} in the DB".format(username))
        return jsonify(message="{0} added successfully".format(username)), 200
    except pymongo.errors.DuplicateKeyError as e:
        logger.exception('{0}'.format(e))
        return jsonify(message="Username already taken, please choose another one"), 400
    except Exception as e:
        logger.exception('{0}'.format(e))
        return jsonify(message="Server Exception. Try again in some time"), 500


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
    db_obj = CollectionClass(mongo.db[collection]).find_one(filter={'$or': [{'username': user}, {'email': user}]})
    if db_obj is not None:
        decrypted_password = cipher_obj.decrypt(db_obj['password']).decode('utf-8')
        if json_data.get('password') == decrypted_password:
            logger.info('User Credentials Authentication Successful')
            return jsonify(message="User Credentials Authentication Successful"), 200
        else:
            logger.warning('Wrong Password')
            return jsonify(message="Invalid Username or Password"), 400
    else:
        logger.info('Invalid Username')
        return jsonify(message="Invalid Username or Password"), 400
