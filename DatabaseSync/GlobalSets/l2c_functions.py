#!/usr/bin/env python3

# Global imports
from .Mongo import Clients as MongoClient, DataBases as db, DashboardCollections as col

# Import librarys
from pymongo import collection, errors
from bson import ObjectId
import bson, json, datetime

def documentHandler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)

def syncronize(collection: str):
    pipeline = [
        {
            '$project': {
                '_id': 1
            }
        }
    ]
    Local = json.loads(json.dumps(list(MongoClient.LocalClient[db.dbDashboard][collection].aggregate(pipeline=pipeline)),default=documentHandler))
    Cloud = json.loads(json.dumps(list(MongoClient.CloudClient[db.dbDashboard][collection].aggregate(pipeline=pipeline)),default=documentHandler))

    idLocal = [i['_id'] for i in Local]
    idCloud = [i['_id'] for i in Cloud]

    for i in idLocal:
        for j in idCloud:
            if i == j:
                idLocal.remove(i)
                idCloud.remove(j)

    for id in idCloud:
        try:
            if MongoClient.CloudClient.is_primary:
                MongoClient.CloudClient[db.dbDashboard][collection].delete_one({'_id': ObjectId(id)})
        except Exception as e:
            eStr = str(e)
            print(eStr) 

    for id in idLocal:
        try:
            document =  MongoClient.LocalClient[db.dbDashboard][collection].find_one({'_id': ObjectId(id)})
            for upTry in range(0,5):
                if MongoClient.CloudClient.is_primary and MongoClient.CloudClient[db.dbDashboard][collection].insert_one(document).acknowledged:
                    break
        except Exception as e:
            eStr = str(e)
            print(eStr)  

    if MongoClient.LocalClient[db.dbDashboard][collection].count_documents({}) != MongoClient.CloudClient[db.dbDashboard][collection].count_documents({}):
        syncronize(collection=collection)