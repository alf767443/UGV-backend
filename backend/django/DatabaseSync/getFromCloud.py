#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db, Collections as col
import GlobalSets.c2l_functions as c2l

# Import librarys
from pymongo import collection, errors
import bson, datetime

def local2cloud():
    while(True):
        for collection in col.Collections:
                c2l.downloadBase(database=db.dbBuffer, collection=collection['name'])

if __name__ == '__main__':
    try:
        print(datetime.datetime.now(), 'Synchronising base')
        local2cloud()
        print(datetime.datetime.now(), 'Synchronising stop')
    except Exception:
        print(datetime.datetime.now(), 'Synchronising stop')
        pass
