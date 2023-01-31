from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


from pymongo import MongoClient

from django.core.files.storage import default_storage

import bson, datetime, json, math

import time

Client = MongoClient('mongodb://localhost:27017/')

def my_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    elif isinstance(x, json.JSONDecodeError):
        print(x)
        return str(x)
    else:
        print(x)
        raise TypeError(x)

def nan2None(obj):
    if isinstance(obj, dict):
        return {k:nan2None(v) for k,v in obj.items()}
    elif isinstance(obj, list):
        return [nan2None(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj

class NanConverter(json.JSONEncoder):
    def default(self, obj):
        my_handler(obj)
        pass
    # def encode(self, obj, *args, **kwargs):
    #     obj = nan2None(obj)
    #     return super().encode(obj, *args, **kwargs)
    # def iterencode(self, obj, *args, **kwargs):
    #     obj = nan2None(obj)
    #     return super().iterencode(obj, *args, **kwargs)

# Query table API
@csrf_exempt
def query(request,query=''):
    if  request.method=='POST':
        raw=JSONParser().parse(request)
        database = raw['database']
        collection = raw['collection']
        pipeline = raw['pipeline']
        result = json.loads(json.dumps(list(Client[database][collection].aggregate(pipeline=pipeline)), default=my_handler, allow_nan=False))
        print(result)
        time.sleep(10)
        
        return JsonResponse(result,safe=False)