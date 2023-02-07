import pymongo, math as rospy
from pymongo import collection
from datetime import datetime

# ---------------------------------------------------
# CLIENTS
class Clients:
    # Local Client
    try:
        LocalClient = pymongo.MongoClient('mongodb://localhost:27017/',)
    except:
        pass

    # Cloud Client
    try:
        CloudClient = pymongo.MongoClient("mongodb+srv://Admin:admin@cedri.hfunart.mongodb.net/?retryWrites=true&w=majority")
    except:
        pass

    # Cloud Client
    try:
        ip      = '192.168.217.183'  # Remote Unit CLient
        port    = 27017             # Port 
        RemoteUnitClient = pymongo.MongoClient('mongodb://' + ip + ':' + str(port) + '/', connectTimeoutMS = 1000, serverSelectionTimeoutMS = 1000, socketTimeoutMS = 1000)
    except:
        pass

# ---------------------------------------------------
# DATASOURCE
class DataSource:
    # CeDRI UGV datasource
    CeDRI_UGV = 'CeDRI_UGV'

# ---------------------------------------------------
# DATABASES
class DataBases:
    # Cloud dashboard database
    dbDashboard = 'CeDRI_UGV_dashboard'

    # Cloud buffer
    dbBuffer    = 'CeDRI_UGV_buffer'

    # Cloud datalake
    dataLake  = 'CeDRI_UGV_datalake'

# ---------------------------------------------------
# COLLECTIONS
class Collections:
    # Collection battery
    Battery         = 'Battery'

    # Collection position odometry
    PositionOdom    = 'Position_Odometry'

    # Collection position amcl
    PositionAMCL    = 'Position_AMCL'

    # Collection position
    Motor           = 'Motor'

    # Collection log
    Log             = 'Log'

    # Collection LiDAR
    LiDAR           = 'LiDAR'

    # Collection Occupancy
    Occupancy       = 'Occupancy'

    # Actions
    Actions         = 'Actions'

    # Connection
    Connection      = 'Connection'

# ---------------------------------------------------
# FUNCTIONS
# Log
def log(logData:str):
    try:
        Clients.LocalClient[DataBases.dataLake][Collections.Log].insert_one({
            "dateTime": datetime.now(),
            "log": logData 
        })
    except:
        pass

# Size of a collection
def sizeOf(database: collection.Collection):
    aggreation =  [
        {
            '$collStats': {
                'storageStats': {}
            }
        }
    ]
    try:
        result = database.aggregate(aggreation)
        result = list(result)[0]['storageStats']['size']
    except Exception as e:
                eStr    = str(e)
                rospy.loginfo(eStr)
    return result

# Delete a random item
def delRandomItem(database: collection.Collection):
    aggreation = [
        {
            '$sample': {
                'size': 1
            }
        }
    ]
    result =  database.aggregate(aggreation)
    while result._has_next():
            temp = result.next()
            try:
                database.delete_one(temp).deleted_count
            except Exception as e:
                eStr    = str(e)
                rospy.loginfo(eStr)
