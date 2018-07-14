#import pymongo
import sys
import re
import time
import pdb

class collectionClass(object):
   def __init__(self,collection_name):
      
      #conn=pymongo.MongoClient()
      #print "Connected to Mongo successfully!!!"
      #self.db = conn["%s" % db_name]
      #try:
      self.collection = collection_name
      #except:
      #   self.db.drop_collection("%s" % collection_name)
      #   self.collection = self.db.create_collection("%s" % collection_name)

   def find(self,filter=None):
      if self.total_docs() == 0:
         print "No Docs found Returning False"
         return False
      if filter != None:
        return list(self.collection.find('%s' % filter))

      return list(self.collection.find())
   
   def insert_many(self,new_doc):
      #if type(new_doc) is not dict:
      #   raise Exception('document type should be dict')
      
      self.collection.insert_many(new_doc)
     
   def count(self):
      return self.collection.count()
   
   def sortAscending(self,key):
      return list(self.collection.find().sort("%s" % key,1))
   
   def sortDescending(self,key)
      return list(self.collection.find().sort("%s" % key,-1))
