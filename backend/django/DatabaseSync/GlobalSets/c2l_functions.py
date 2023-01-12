#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col

# Import librarys
from pymongo import collection, errors
import bson

def downloadElement(document: dict, local: collection.Collection, cloud: collection.Collection):
    try:
        for upTry in range(0,5):
            if MongoClient.LocalClient.is_primary and local.insert_one(document).acknowledged:
                cloud.delete_one(document)
                break
    except errors.DuplicateKeyError:
        cloud.delete_one(document)
    except Exception as e:
        eStr = str(e)
        print(eStr)  


def downloadBase(database: str, collection: str):
    try:
        local = MongoClient.LocalClient[database][collection]
    except Exception as e:
        eStr = str(e)
        print(eStr)
        return
    try:
        cloud = MongoClient.CloudClient[database][collection]
    except Exception as e:
        return

    try:
        if MongoClient.CloudClient.is_primary and cloud.count_documents(filter={}) > 0:
            documents = cloud.aggregate([
                {
                    '$sort': {
                        'dateTime': -1
                    }
                },
                {
                    '$limit': 1000
                }
            ])
            while documents._has_next():
                downloadElement(document=documents.next(), local=local, cloud=cloud)
                       
    except Exception as e:
        eStr = str(e)
        print(eStr)