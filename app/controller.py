import sys
import os
import json
import ast
from flask import render_template, request, Response, jsonify
from flask_script import Manager
from bson.json_util import loads,dumps
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.main import create_app, get_collection_map
from app.main.collection_lib import CollectionClass

app, mongo = create_app('dev')
# if app is None and mongo is None:
#     print "Error in creating Mongo DB connection. Check again"
#
try:
    print mongo.db.collection_names()

except Exception as e:
    print "Could not connect to MongoDB: {0}".format(e)
    sys.exit(1)
manager = Manager(app)


@app.route('/getAll', methods=['GET'])
def find_data():

    print dir(mongo.db)
    collection = mongo.db.list_collection_names()[0]
    document = mongo.db[collection].find()
    demo_data = mongo.db[collection].find({'place': 'San Francisco'})
    # print demo_data,"DEMO"
    # print list(demo_data),"&&&"
    data = list(demo_data)
    print len(data), "**{0}**".format(data), len(list(demo_data))
    for each_data in data:
        print each_data['_id'].generation_time, "*****"

    # print list(document.sort('zipcode',1))

    return dumps(list(document.sort('zipcode', -1)))

#####################################################################################################
#Signup Post Routine : returns username,password with code=200 if new user
#                      else returns Username Taken msg with code=400
#####################################################################################################
@app.route('/signup', methods=['POST'])
def signup():
    collection = get_collection_map('user')
    print collection
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
        print "Username taken"
        return jsonify(message="Username already taken, please choose another one"), 400

#####################################################################################################
#Signin Post Routine : returns Valid user with code=200 if username/email and password matches
#                      else returns Invalid username/password with code=400
#####################################################################################################
@app.route('/signin', methods=['POST'])
def signin():
    collection = get_collection_map('user')
    print collection
    json_data = json.loads(request.data)
    username = json_data.get('username')
    #email_id = json_data.get('email')
    # password = json_data.get('password')
    # return jsonify(status="Bad"), 500
    user_obj = CollectionClass(mongo.db[collection]).find_one({'username': username})
    email_obj = CollectionClass(mongo.db[collection]).find_one({'email': username})
    if (user_obj!= None or email_obj!=None):
        if json_data.get('password') == user_obj['password']:
            return jsonify(message="Valid User"), 200
       else:
            return jsonify(message="Wrong Password"),400 
    else:
        print "Username Invalid"
        return jsonify(message="Invalid Username"), 400
 

#Sample HTTP error handling

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404


if __name__ == '__main__':
    manager.run()
