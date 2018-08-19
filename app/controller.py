import sys
import os
from flask import jsonify
from flask_script import Manager
from bson.json_util import loads,dumps
import json
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.main import logger, app, mongo
from app.views.users import user_mod
from app.views.articles import articles_mod

from flask_cors import cross_origin

app.register_blueprint(user_mod)
app.register_blueprint(articles_mod)


try:
    logger.debug("Trying to test if DB can be connected or not by displaying all the collection names: {0}".format(mongo.db.collection_names()))
except Exception as e:
    logger.exception("Could not connect to MongoDB Exiting... {0}".format(e))
    sys.exit(1)

manager = Manager(app)


@app.route('/getAll', methods=['GET'])
@cross_origin()
def find_data():

    # print dir(mongo.db)
    collection = mongo.db.list_collection_names()[0]
    collection = 'demo-articles'
    document = mongo.db[collection].find()
    # document = mongo.db[collection].find({'article_title': 'USC'})
    demo_data = mongo.db[collection].find({'article_title': 'San Francisco'})
    # print demo_data,"DEMO"
    # print list(demo_data),"&&&"
    data = list(demo_data)
    # print (list(document))
    # print len(data), "**{0}**".format(data), len(list(demo_data))
    # for each_data in data:
    #     print each_data['_id'].generation_time, "*****"

    # print list(document.sort('zipcode',1))
    # return jsonify(message=list(document))
    data = [each_article for each_article in document]
    last_id = data[-1]["_id"]
    # print (type(last_id))
    # print (dumps(data))
    # print (type(dumps(data)))
    return_dict = {}
    return_dict["message"]=dumps(data)
    return_dict["last_id"]=dumps(last_id)
    print (dumps(last_id), type (loads(dumps(last_id))))
    # print((last_id["$oid"]))
    print (json.loads(dumps(last_id)), json.loads(dumps(last_id))["$oid"])
    # print(return_dict)
    # return dumps(return_dict), 202
    return dumps(data) ,203
    # return jsonify(message=dumps(data),
    #                last_id=dumps(last_id)), 200


    # return dumps(list(document.sort('zipcode', -1)))


#Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    logger.warning('{0}'.format(error))
    return jsonify(message="{0}".format(error)), 404
    # return render_template('404.html', error=error), 404


if __name__ == '__main__':
    #Entry point
    manager.run()
