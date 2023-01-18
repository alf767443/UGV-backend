#!/usr/bin/env python3

# Global imports
from GlobalSets.Mongo import Clients as MongoClient, DataBases as db

# Import librarys
from pymongo import collection, errors
import bson, datetime, json, bson, time

def documentHandler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)


pipelineCol = MongoClient.LocalClient[db.dbDashboard]['pipelines']

def newPipeline(name: str, database: str, collection: str, pipeline: dict):
    document = {
        'name' : name,
        'database': database,
        'collection': collection,
        'pipeline' : pipeline
    }
    try:
        if pipelineCol.insert_one(document=document).acknowledged:
            print('Added')
    except Exception as e:
        eStr = str(e)
        print(eStr)

def executePipelines():
    while (True):
        time.sleep(1)
        pipelines = json.loads(json.dumps(list(pipelineCol.find({})),default=documentHandler))
        for pipeline in pipelines:
            print("\rApplying pipeline: " + pipeline['name'], end='')
            MongoClient.LocalClient[pipeline['database']][pipeline['collection']].aggregate(pipeline=pipeline['pipeline'])

if __name__ == '__main__':
    try:
        print(datetime.datetime.now(), 'Applying pipelines start')
        executePipelines()
        print(datetime.datetime.now(), 'Applying pipelines stop')
    except Exception:
        print(datetime.datetime.now(), 'Applying pipelines stop')
        pass
