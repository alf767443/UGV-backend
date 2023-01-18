import pymongo, bson, json, os
from datetime import datetime

# ---------------------------------------------------
# CLIENTS
class Clients:
    # Local Client
    try:
        LocalClient = pymongo.MongoClient('mongodb://localhost:27017/')
    except:
        pass

    # Cloud Client
    try:
        CloudClient = pymongo.MongoClient("mongodb+srv://Admin:admin@cedri.hfunart.mongodb.net/?retryWrites=true&w=majority")
    except:
        pass

    UGV = '10.42.0.1'
# ---------------------------------------------------
# DATABASES
class DataBases:
    # Cloud dashboard database
    dbDashboard = 'CeDRI_UGV_dashboard'

    # Cloud buffer
    dbBuffer    = 'CeDRI_UGV_buffer'

# ---------------------------------------------------
# COLLECTIONS
class Collections:
    # Collection battery
    Battery     = 'Battery_Data'

    # Collection position
    Position    = 'Position_Data'

    # Collection log
    Log         = 'Log'

    # Collection UGV connection
    UGVconnec   = 'UGV_Connection' 

    #
    Collections = [
        {
            'name'              : Battery,
            'maxBufferSize'     : 2e5,      #bytes
            'maxBufferCloud'    : 1e5,      #bytes
            'maxDashboardSize'  : 100       #Itens
        },
        {
            'name'              : Position,
            'maxBufferSize'     : 2e5,      #bytes
            'maxBufferCloud'    : 1e5,      #bytes
            'maxDashboardSize'  : 100       #Itens
        },
        {
            'name'              : Log,
            'maxBufferSize'     : 1e2,      #bytes
            'maxBufferCloud'    : 1e2,      #bytes
            'maxDashboardSize'  : 100       #Itens
        },
        {
            'name'              : UGVconnec
        }
    ]

# ---------------------------------------------------
# DASHBOARD COLLECTIONS
class DashboardCollections:
    Collections = [
        {
            'name'              : 'Battery_actual',
            'maxLength'         :  1
        },
        {
            'name'              : 'pipelines',
            'maxLength'         :  1000
        }
    ]

