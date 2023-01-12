from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.renderers import JSONRenderer
from pymongo import MongoClient
import json, bson

from ActionsApplication.models import *
from ActionsApplication.serializers import *

from django.core.files.storage import default_storage

QueueDB = MongoClient('mongodb://localhost:27017/')['CeDRI_UGV']['ActionsApplication_queue']

# Actions API
@csrf_exempt
def actionsApi(request,id=0):
    if request.method=='GET':
        actions = Actions.objects.all()
        actions_serializer=ActionsSerializer(actions,many=True)
        return JsonResponse(actions_serializer.data,safe=False)
    elif request.method=='POST':
        actions_data=JSONParser().parse(request)
        actions_serializer=ActionsSerializer(data=actions_data)
        if actions_serializer.is_valid():
            actions_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        actions_data=JSONParser().parse(request)
        actions=Actions.objects.get(ActionsId=actions_data['ActionsId'])
        actions_serializer=ActionsSerializer(actions,data=actions_data)
        if actions_serializer.is_valid():
            actions_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        actions=Actions.objects.get(ActionsId=id)
        actions.delete()
        return JsonResponse("Deleted Successfully",safe=False)

@csrf_exempt
def queueApi(request,id=0):
    if request.method=='GET':
        queue = QueueDB.aggregate([
            {
                '$sort': {
                    'QueueNumber': 1
                }
            }, {
                '$lookup': {
                    'from': 'ActionsApplication_actions', 
                    'localField': 'Action_id', 
                    'foreignField': '_id', 
                    'as': 'Action'
                }
            }, {
                '$unwind': '$Action'
            }, {
                '$unset': [
                    '_id', 'Action_id', 'Action._id'
                ]
            }
        ])
        result = list(queue)
        return JsonResponse(result,safe=False)
    elif request.method=='POST':
        queue_data=JSONParser().parse(request)        
        data = {
            "QueueNumber" : queue_data['QueueNumber'],
            "Action_id": bson.ObjectId(queue_data['Action'])
        }
        print(data)
        try:
            QueueDB.insert_one(data)
            return JsonResponse("Added Successfully",safe=False)
        except:
            return JsonResponse("Failed to Add",safe=False)
    elif request.method=='DELETE':
        queue=Queue.objects.get(QueueId=id)
        queue.delete()
        return JsonResponse("Deleted Successfully",safe=False)
