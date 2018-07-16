import logging

class CollectionClass(object):
    def __init__(self, collection_name):
        self.collection = collection_name
        self.logger = logging.getLogger(__name__)

    def find_one(self, keyword=None):
        '''
        :param keyword: Dict obj to search for in the collections
        :return: 
        '''
        self.logger.info('Trying to find {0} in DB'.format(keyword))
        return self.collection.find_one(keyword)

    def find(self, keyword=None):
        if self.count() == 0:
            self.logger.info('Could not retrieve {0} in {1} collections. Returning False'.format(keyword, self.collection))
            # print "No Docs found. Returning False"
            return False
        if keyword is not None:
            self.logger.info('Executing find only for {0}'.format(keyword))
            return list(self.collection.find('%s' % keyword))

        self.logger.info('Trying to do similar to SELECT *')
        return list(self.collection.find())

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

    def count(self):
        return self.collection.count()

    def sort_ascending(self, key):
        self.logger.info('Sort the result in ascending order for {0}'.format(key))
        return list(self.collection.find().sort("%s" % key, 1))

    def sort_descending(self, key):
        self.logger.info('Sort the result in ascending order for {0}'.format(key))
        return list(self.collection.find().sort("%s" % key, -1))
