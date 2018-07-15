class CollectionClass(object):
    def __init__(self, collection_name):
        # conn=pymongo.MongoClient()
        # print "Connected to Mongo successfully!!!"
        # self.db = conn["%s" % db_name]
        # try:
        self.collection = collection_name
        # except:
        #   self.db.drop_collection("%s" % collection_name)
        #   self.collection = self.db.create_collection("%s" % collection_name)

    def find_one(self, keyword=None):
        return self.collection.find_one(keyword)

    def find(self, keyword=None):
        if self.count() == 0:
            print "No Docs found. Returning False"
            return False
        if keyword is not None:
            return list(self.collection.find('%s' % keyword))

        return list(self.collection.find())

    def insert_many(self, new_doc):
        # if type(new_doc) is not dict:
        #   raise Exception('document type should be dict')
        return_value = True
        try:
            self.collection.insert_many(new_doc)
        except Exception as e:
            print e
            return_value = False

        return return_value

    def count(self):
        return self.collection.count()

    def sort_ascending(self, key):
        return list(self.collection.find().sort("%s" % key, 1))

    def sort_descending(self, key):
        return list(self.collection.find().sort("%s" % key, -1))
