#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, DashboardCollections as col
import GlobalSets.l2c_functions as l2c

# Import librarys
from pymongo import collection, errors
import bson, datetime

def syncBases():
    while(True):
        for collection in col.Collections:
            print("\rSynchronising the collection: " + collection['name'], end='')
            l2c.syncronize(collection=collection['name'])
                

if __name__ == '__main__':
    try:
        print(datetime.datetime.now(), 'Synchronising base')
        syncBases()
        print(datetime.datetime.now(), 'Synchronising stop')
    except Exception:
        print(datetime.datetime.now(), 'Synchronising stop')
        pass
