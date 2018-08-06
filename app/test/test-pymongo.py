# from app.main import logger, get_collection_map, mongo
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from app.main import mongo, pymongo
from app.main.collection_lib import CollectionClass
from app.main import logger as log
import random
import string

def populate_db():

    test_document_list = list()
    for _ in range(50):
        username = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        email = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        test_document_list.append({'username' : username, 'email' : email})

    print (test_document_list)
    collection_without_index = "test_without_index"
    collection_with_index = "test_with_index"

    CollectionClass(mongo.db[collection_without_index]).insert_many(test_document_list)
    CollectionClass(mongo.db[collection_with_index]).insert_many(test_document_list)


def create_index():
    collection_with_index = "test_with_index"
    log.debug("Trying To create index for {0}".format(collection_with_index))
    print (mongo.db[collection_with_index].create_index([("username", 1)], unique=True))
    print (mongo.db[collection_with_index].create_index([("email", 1)]))

def output():
    collection_without_index = "test_without_index"
    collection_with_index = "test_with_index"

    total_number_of_doc = mongo.db[collection_without_index].find().count()
    print("Total doc present in the collection WITHOUT an index: {0}"
    .format(total_number_of_doc))

    without_index_cursor = mongo.db[collection_without_index].find({'email': 'qsxfinltag'}).explain()
    print("Trying to find the document where username == TDOVHGGDOL")
    print("Execution Success? {0}".format(without_index_cursor['executionStats']['executionSuccess']))
    print("Documents Returned? {0}".format(without_index_cursor['executionStats']['nReturned']))
    print("Documents Scanned? {0}".format(without_index_cursor['executionStats']['totalDocsExamined']))

    print ("*********************************************************************************")
    total_number_of_doc = mongo.db[collection_with_index].find().count()
    print("\nTotal doc present in the collection WITH an index: {0}"
          .format(total_number_of_doc))

    without_index_cursor = mongo.db[collection_with_index].find({'email': 'qsxfinltag'}).explain()
    print("Trying to find the document where username == TDOVHGGDOL")
    print("Execution Success? {0}".format(without_index_cursor['executionStats']['executionSuccess']))
    print("Documents Returned? {0}".format(without_index_cursor['executionStats']['nReturned']))
    print("Documents Scanned? {0}".format(without_index_cursor['executionStats']['totalDocsExamined']))


def test_unique():
    collection_with_index = "test_with_index"
    try:
        cursor = mongo.db[collection_with_index].insert({'username': 'TDOVHGGDOL', 'email': 'qsxfinltag'})
    except pymongo.errors.DuplicateKeyError as e:
        print ("{0}".format(e))


def populate_articles_collection():
    # "5b4a9bb171325e2dba25e78e" --> kapil
    # "5b4aa02e71325e2ee7b566e6" --> hansal
    # "5b4ab0d52db4283921ab7b7a" ---> gareth
    pass

if __name__ == '__main__':
    # populate_db()
    create_index()
    # output()
    # test_unique()
    # output()