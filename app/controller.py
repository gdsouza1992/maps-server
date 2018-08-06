import sys
import os
from flask import jsonify
from flask_script import Manager
from bson.json_util import loads,dumps
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
    document = mongo.db[collection].find()
    demo_data = mongo.db[collection].find({'place': 'San Francisco'})
    # print demo_data,"DEMO"
    # print list(demo_data),"&&&"
    data = list(demo_data)
    # print len(data), "**{0}**".format(data), len(list(demo_data))
    # for each_data in data:
    #     print each_data['_id'].generation_time, "*****"

    # print list(document.sort('zipcode',1))

    return dumps(list(document.sort('zipcode', -1)))


#Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    logger.warning('{0}'.format(error))
    return jsonify(message="{0}".format(error)), 404
    # return render_template('404.html', error=error), 404


if __name__ == '__main__':
    #Entry point
    manager.run()
