from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status


from pymongo import MongoClient

from django.core.files.storage import default_storage

import bson, datetime, json, math, numpy

import time

Client = MongoClient('mongodb://localhost:27017/')

def my_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    elif isinstance(x, float) and math.isnan(x):
        return None
    else:
        print(x)
        print('_______________________________________________________________________________________________________')
        raise TypeError(x)

def nan2None(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, bson.objectid.ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
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
    def encode(self, obj, *args, **kwargs):
        obj = nan2None(obj)
        return super().encode(obj, *args, **kwargs)
    def iterencode(self, obj, *args, **kwargs):
        obj = nan2None(obj)
        return super().iterencode(obj, *args, **kwargs)

# Query table API
@csrf_exempt
def chart(request, query=''):
    print(request)
    # print(JSONParser().parse(request))
    if  request.method=='GET':
        try:
            name = request.GET.get('name','')
            # print(request.GET.get)
            
            # raw=JSONParser().parse(request)
            # print(raw)
            # name = raw['name']
            # print(1)
            result = MongoClient.RemoteUnitClient['CeDRI_UGV_dashboard']['graphs'].find_one(filter={'name': name})
            print(result)
            query = result['query'] 
            print(query)
            result = json.loads(json.dumps(list(Client[query['database']][query['collection']].aggregate(pipeline=query['pipeline'])), cls=NanConverter, allow_nan=False))   
            # print(1)
            return JsonResponse(result,safe=False)
            # return Response({'Invalid Requisition'}, status=status.HTTP_200_OK)
        except:
            return JsonResponse({},safe=False)
            # return Response({'Invalid Requisition'}, status=status.HTTP_400_BAD_REQUEST)
        

@csrf_exempt
def query(request,query=''):
    if  request.method=='POST':
        raw=JSONParser().parse(request)
        database = raw['database']
        collection = raw['collection']
        pipeline = raw['pipeline']
        result = json.loads(json.dumps(list(Client[database][collection].aggregate(pipeline=pipeline)), cls=NanConverter, allow_nan=False))        
        return JsonResponse(result,safe=False)

# First connect with UGV
@csrf_exempt
def firstConnection(request,query=''):
    if  request.method=='POST':
        raw=JSONParser().parse(request)
        print(raw)
        result = {
            "timedate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return JsonResponse(result,safe=False)
    
# Save dashboard info
@csrf_exempt
def updateDocument(request,query=''):
    if  request.method=='POST':
        raw=JSONParser().parse(request)
        database = raw['database']
        collection = raw['collection']
        # pipeline = raw['pipeline']
        filter = raw['filter']
        update = raw['update']
        print(raw)
        print(database)
        print(collection)
        print(type(filter), filter)
        print(type(update), update)
        result = json.loads(json.dumps(list(Client[database][collection].find_one_and_update(upsert=True, filter=filter, update=update ))))
        print(result)
        return JsonResponse(result,safe=False)