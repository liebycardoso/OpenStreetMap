# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 16:12:26 2016

@author: MasterLieby
"""
#mongoimport --db users --collection contacts --file contacts.json

from pymongo import MongoClient
import json
import codecs

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mapbh



def insert_tweet(infile, db):
    #db.twitter1.remove()
    num_mapbh = db.mapbh.find().count()
    print "num_reg before:", db.mapbh.count()
    
    data = []
    # open the json, with the correct formatting
    with codecs.open(infile,'rU','utf-8') as f:
        # read each line of the json
        for line in f:
            # add each item to a list
           data.append(json.loads(line))

    db.mapbh.insert(data)
    print db.mapbh.find_one()
    num_mapbh = db.mapbh.count()
    print "num_reg after:", db.mapbh.find().count()
  
if __name__ == "__main__":
    # Code here is for local use on your own computer.
    insert_tweet('C:/Nanodegree/MongoDb/Trab_final/mapbh.json', db)