#!/usr/bin/env python  
#-*- coding:utf-8 -*-

import pymongo

client = pymongo.MongoClient(host='localhost')
db = client.zhihu

collection = db.users
# print(collection.find().count())
results = collection.find().sort("name",pymongo.ASCENDING).skip(2).limit(20)
for i in results:
    print(i)
client.close()