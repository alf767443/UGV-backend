from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer


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

# Chart requests
@csrf_exempt
def chart(request, query=''):
    MDBchart =  Client['CeDRI_dashboard']['charts']
    if  request.method =='GET':
        try:
            name = request.GET.get('name','')
            result = MDBchart.find_one(filter={'name': name})
            query = result['query'] 
            database = query['database']
            collection = query['collection']
            pipeline = query['pipeline']
            option = result['option']
            tile = result['tile']
            data = json.loads(json.dumps(list(Client[database][collection].aggregate(pipeline=pipeline)), cls=NanConverter, allow_nan=False)) 
            result = {'data': data, 'option': option, 'tile': tile, 'query': query}
            return JsonResponse(data=result,safe=False, status=status.HTTP_302_FOUND)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        try:
            raw=JSONParser().parse(request)
            result = MDBchart.insert_one(raw).inserted_id
            update = {'$set': {'name': str(result)}}
            filter = {'_id':  bson.ObjectId(result)}
            result = json.loads(json.dumps(list(MDBchart.find_one_and_update(upsert=True, filter=filter, update=update)), cls=NanConverter, allow_nan=False))
            return JsonResponse(data=result,safe=False, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PUT':
        try:
            raw=JSONParser().parse(request)
            filter = raw['filter']
            update = raw['update']
            result = json.loads(json.dumps(list(MDBchart.find_one_and_update(upsert=True, filter=filter, update=update)), cls=NanConverter, allow_nan=False))
            return JsonResponse(data=result,safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        try:
            raw=JSONParser().parse(request)
            filter = raw['filter']
            result = json.loads(json.dumps(list(MDBchart.delete_one(upsert=True, filter=filter)), cls=NanConverter, allow_nan=False))
            return JsonResponse(data=result,safe=False, status=status.HTTP_301_MOVED_PERMANENTLY)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'OPTIONS':
        try:
            raw=JSONParser().parse(request)
            print(raw)
            pipeline = raw['pipeline']
            print(pipeline)
            result = json.loads(json.dumps(list(MDBchart.aggregate(pipeline=pipeline)), cls=NanConverter, allow_nan=False))
            print(result)
            return JsonResponse(data=result,safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return JsonResponse({'data': 'Method not allowed'},safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
# Robots requests
@csrf_exempt
def robot(request, query=''):
    MDBchart =  Client['CeDRI_dashboard']['robots']
    if  request.method =='GET':
        try:
            name = request.GET.get('name','')
            print(name)
            if name == '':
                result = json.loads(json.dumps(list(MDBchart.find({})), cls=NanConverter, allow_nan=False))   
                print(result)
            else:
                result = json.loads(json.dumps(MDBchart.find_one({'name': name}), cls=NanConverter, allow_nan=False))   
                print(result)
            return JsonResponse(data=result,safe=False, status=status.HTTP_302_FOUND)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        try:
            raw=JSONParser().parse(request)
            result = MDBchart.insert_one(raw).inserted_id
            update = {'$set': {'name': str(result)}}
            filter = {'_id':  bson.ObjectId(result)}
            result = json.loads(json.dumps(list(MDBchart.find_one_and_update(upsert=True, filter=filter, update=update)), cls=NanConverter, allow_nan=False))
            return JsonResponse(data=result,safe=False, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PUT':
        try:
            raw=JSONParser().parse(request)
            print(raw)
            filter = raw['filter']
            print(filter)
            update = raw['update']
            print(update)
            result = json.loads(json.dumps(list(MDBchart.find_one_and_update(upsert=True, filter=filter, update=update)), cls=NanConverter, allow_nan=False))
            print(result)
            return JsonResponse(data=result,safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        try:
            print(request)
            raw=JSONParser().parse(request)
            print(raw)
            filter = raw['filter']
            result = json.loads(json.dumps(list(MDBchart.delete_one(upsert=True, filter=filter)), cls=NanConverter, allow_nan=False))
            print(result)
            return JsonResponse(data=result,safe=False, status=status.HTTP_301_MOVED_PERMANENTLY)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'OPTIONS':
        try:
            raw=JSONParser().parse(request)
            filter = {
                'robot': raw['robot']
            }
            result = MDBchart.find_one(filter=filter, projection={'robot': 1, 'password': 1, 'name': 1})
            if raw['robot'] == result['robot'] and raw['password'] == result['password']:
                return JsonResponse(data={'name': result['name']},safe=False, status=status.HTTP_202_ACCEPTED)
            else:
                return JsonResponse(data={},safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return JsonResponse({'error': type(e).__name__, 'args': e.args},safe=False, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'data': 'Method not allowed'},safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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