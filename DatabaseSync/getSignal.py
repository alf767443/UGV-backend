from GlobalSets.Mongo import Clients, DataBases as db, Collections as col
from tcppinglib import tcpping
import datetime, socket

ip      = '127.0.0.1' #Clients.UGV
port    = 27017

def getInfo(ip: str, port: int):
    try:
        ping = tcpping(address=ip, port=port, interval=1, timeout=2, count=5)
        tcpping('127.0.0.1')
    except Exception as e:
        print(e)

    return(ping.is_alive, ping.avg_rtt)

def saveSignalRTT():
    while True:
        try:
            (isAlive , RTT) = getInfo(ip=ip, port=port)
            data = {
                'dateTime': datetime.datetime.now(),
                'Connect': isAlive,
                'RTT': RTT
            }
            Clients.LocalClient[db.dbBuffer][col.UGVconnec].insert_one(data)
        except Exception as e:
            print(e)



if __name__ == '__main__':
    try:
        print(datetime.datetime.now(), 'Start get signal with UGV')
        saveSignalRTT()
        print(datetime.datetime.now(), 'Stop get signal with UGV')
    except Exception:
        print(datetime.datetime.now(), 'Stop get signal with UGV')
        pass
