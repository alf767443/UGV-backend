#!/usr/bin/env python3

from background_task import background
from .backgroudTask import backgroudTask  # Importe a função backgroudTask do seu arquivo

@background(schedule=10)  # Defina o tempo de espera desejado em segundos
def execute_background_task():
    backgroudTask()  # Chame a função backgroudTask no seu arquivo