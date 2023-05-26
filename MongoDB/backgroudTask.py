#!/usr/bin/env python3

import math, bson, json, datetime, time, asyncio, threading
from pymongo import MongoClient

Client = MongoClient('mongodb://localhost:27017/')

Scripts = Client['CeDRI_dashboard']['scripts']
Logs = Client['CeDRI_dashboard']['logs']
threads = []

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

def log(robot, script, msg, type):
    out = {
        'script': script,
        'robot': robot,
        'msg': msg,
        'type': type,
        'datetime': datetime.datetime.now()
    }
    Logs.insert_one(document=out).acknowledged

def rospub(robot, topic, comand):
    return True

def action(robot, command):
    return True

def updateCode(metaCode, set):
    return Scripts.update_one(filter={'name': metaCode['name']}, update={'$set': set}).acknowledged

def nextExec(metaCode):
    _now = datetime.datetime.now()
    set = {
        'next':_now + datetime.timedelta(seconds=metaCode['sample']), 
        'last': _now
    }
    updateCode(metaCode=metaCode, set=set)

def statusExec(metaCode, status):
    set = {
        'status': status
    }
    return updateCode(metaCode=metaCode, set=set)

def runCode(metaCode):
    try:
        _id = metaCode['name']
        code = metaCode['code']
        robot = metaCode['robot']     
        code = code.replace('log(', 'log(robot="' + robot + '",script="' + _id + '",' )
    except Exception as e:
        log(robot=robot, msg=e,type='error')
        statusExec(metaCode=metaCode, status='error')

    try:
        code = compile(code, "<string>", "exec")
    except Exception as e:
        log(robot=robot, msg=e,type='error')
        statusExec(metaCode=metaCode, status='error')

    try:
        statusExec(metaCode=metaCode, status='run')
        exec(code)
        if Scripts.find_one(filter={'name': metaCode['name']})['status'] == 'run':
            statusExec(metaCode=metaCode, status='wait')
    except Exception as e:
        log(robot=robot, msg=e,type='error')
        statusExec(metaCode=metaCode, status='error')

def nextSleep(max = 10):
    pipeline = [
        {
            '$match': {
                'status': {
                    '$ne': 'error'
                }
            }
        }, {
            '$group': {
                '_id': None, 
                'next': {
                    '$min': '$next'
                }
            }
        }
    ]
    nextExe = list(Scripts.aggregate(pipeline=pipeline))[0]['next'].timestamp()
    now = datetime.datetime.now().timestamp()
    wait = (nextExe - now)*(nextExe > now)
    if wait > 10:
        wait = 10
    if wait < 1: 
        wait = 1
    return wait

def runCodeAsync(metaCode):
    thread = threading.Thread(target=runCode, args=(metaCode,))
    thread.setName(metaCode['name'])
    thread.daemon = True
    thread.start()
    _thread = {
        'thread': thread,
        'name': metaCode['name']
    }
    threads.append(_thread)

def cleanThreads():
    for thread in threads:
        if not thread['thread'].is_alive():
            threads.remove(thread)
    return True

def stopThread(metaCode):
    _threads = [thread for thread in threads if thread.get('name') == metaCode['name']]
    for thread in _threads:
        thread['thread'].join()

