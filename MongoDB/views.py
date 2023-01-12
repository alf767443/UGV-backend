from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


from pymongo import MongoClient

from django.core.files.storage import default_storage

import bson, datetime, json

Client = MongoClient('mongodb://localhost:27017/')

def my_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)

# Query table API
@csrf_exempt
def query(request,query=''):
    if  request.method=='POST':
        raw=JSONParser().parse(request)
        database = raw['database']
        collection = raw['collection']
        pipeline = raw['pipeline']
        result = json.loads(json.dumps(list(Client[database][collection].aggregate(pipeline=pipeline)),default=my_handler))
        return JsonResponse(result,safe=False)