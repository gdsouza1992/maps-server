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

   def get_all_objects(self):
      if self.total_docs() == 0:
         print "No Docs found Returning False"
         return False

      return self.collection.find()
   
   def insert(self,new_doc):
      #if type(new_doc) is not dict:
      #   raise Exception('document type should be dict')
      
      self.collection.insert_many(new_doc)
     
   def total_docs(self):
      return self.collection.count()
   
   def sort(self,key,direction="Ascending"):
      if direction.lower() == "descending":
         return self.collection.find().sort("%s" % key,pymongo.DESCENDING)
      else:
         return self.collection.find().sort("%s" % key,pymongo.ASCENDING)

