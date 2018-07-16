import logging

class CollectionClass(object):
    def __init__(self, collection_name):
        self.collection = collection_name
        self.logger = logging.getLogger(__name__)

################################################################################################
#   find_one : param keyword : Dict obj to search for in the collections
#            : returns       : None if keyword not found else returns a dict where keyword was found
#################################################################################################
    def find_one(self, keyword=None):

        self.logger.info('Trying to find {0} in DB'.format(keyword))
        return self.collection.find_one(keyword)

################################################################################################
#   find : param keyword : Dict obj to search for in the collections
#        : returns       : all the docs pertaining to that collection if keyword=None
#                          dict if keyword found and if keyword!=None else returns None
#################################################################################################
    def find(self, keyword=None):

        self.logger.info('Trying to do similar to SELECT *')
        return list(self.collection.find(filter='%s' % keyword))

################################################################################################
#   insert_many : param new_doc : document to be added to collection
#               : returns       : cursor if success else returns False
#################################################################################################
    def insert_many(self, new_doc):
        # if type(new_doc) is not dict:
        #   raise Exception('document type should be dict')
        return_value = True
        try:
            self.collection.insert_many(new_doc)
        except Exception as e:
            self.logger.exception('Error while inserting too many docs. {0}'.format(e))
            print e
            return_value = False

        return return_value

################################################################################################
#   count : params None
#         : returns : total number of docs in a collection
#################################################################################################
    def count(self):
        return self.collection.count()

################################################################################################
#   sort_ascending : params key : Key on which the docs in collection will to be sorted
#                  : returns    : Sorted collection of docs in acsending order based on key
#################################################################################################
    def sort_ascending(self, key):
        self.logger.info('Sort the result in ascending order for {0}'.format(key))
        return list(self.collection.find().sort("%s" % key, 1))

################################################################################################
#   sort_descending : params key : Key on which the docs in collection will to be sorted
#                   : returns    : Sorted collection of docs in descending order based on key
#################################################################################################
    def sort_descending(self, key):
        self.logger.info('Sort the result in ascending order for {0}'.format(key))
        return list(self.collection.find().sort("%s" % key, -1))
