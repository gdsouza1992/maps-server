import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.main import create_app
from bson.json_util import dumps
from flask_script import Manager
from flask import render_template

app,mongo = create_app('dev')
# if app is None and mongo is None:
#     print "Error in creating Mongo DB connection. Check again"
#
try:
    print mongo.db.collection_names()

except Exception as e:
    print "Could not connect to MongoDB: {0}".format(e)
    sys.exit(1)
manager = Manager(app)

@app.route('/getAll')
def find_data():
    print dir(mongo.db)
    collection = mongo.db.list_collection_names()[0]
    document = mongo.db[collection].find()
    return dumps(list(document))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404


if __name__ == '__main__':
    manager.run()