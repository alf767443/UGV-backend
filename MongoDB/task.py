#!/usr/bin/env python3

from background_task import background
from .backgroudTask import *  # Importe a função backgroudTask do seu arquivo

@background(schedule=10)  # Defina o tempo de espera desejado em segundos
def execute_background_task():
    while True:
        cleanThreads()
        codes = list(Scripts.find(filter={}))
        for code in codes:
            try:
                if(code['status'] == 'stop' or code['status'] == 'error'):
                    stopThread(metaCode=code)
                if datetime.datetime.now() > code['next'] and code['status'] == 'wait':
                    nextExec(metaCode=code)
                    runCodeAsync(metaCode=code)
            except Exception as e:
                log(robot=code['name'], msg=e,type='error')
                statusExec(metaCode=code, status='error')
        time.sleep(nextSleep())
