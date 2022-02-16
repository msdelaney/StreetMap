# -*- coding: utf-8 -*-

import pprint

def get_db(db_name):
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db
    
db = get_db('osm')

#db.Chat.remove({})

#print db.Chat.find().count()

#print db.Chat.find({"type":"node"}).count()

#print db.Chat.find({"type":"way"}).count()

#print len(db.Chat.distinct("created.user"))

#results = db.Chat.aggregate([{"$match":{"address.postcode":{"$exists":1}}}, {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, {"$sort":{"count":-1}}])

#results = db.Chat.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count": -1 }}, {"$limit":3}])
'''
results = db.Chat.aggregate([
  {"$group":{"_id":"$created.user", "count":{"$sum":1}}},
  {"$group":{"_id":"$count", "num_users":{"$sum":1}}},
  {"$sort":{"_id":1}},
  {"$limit":1}
  ])
'''
'''
results = db.Chat.aggregate([
  {"$match":{"amenity":{"$exists":1}}},
  {"$group":{"_id":"$amenity", "count":{"$sum":1}}},
  {"$sort":{"count": -1}},
  {"$limit":10}
])
'''
'''
results = db.Chat.aggregate([
  {"$match":{"amenity":{"$exists":1}, "amenity":"place_of_worship"}},
  {"$group":{"_id":"$religion", "count":{"$sum":1}}},
  {"$sort":{"count":-1}},
  {"$limit":1}
])
'''

results = db.Chat.aggregate([
  {"$match":{"amenity":{"$exists":1}, "amenity":"restaurant"}},
  {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
  {"$sort":{"count":-1}},
  {"$limit":3}
])
#print results
results_list = [res for res in results]

pprint.pprint(results_list)