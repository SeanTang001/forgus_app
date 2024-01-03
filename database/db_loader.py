import pymongo
from pymongo import MongoClient
import datetime
import json
import os
import time
import security
import random

###############################################################################
########################### LOCATION ENTRY FUNCTIONS ##########################
###############################################################################

def add_location(client, locations):
    for i in locations:
        client["forgus"]["devices"].update({"uid":i["uid"]}, i, True)
        try:
            client["forgus"].create_collection(i["location"])
        except:
            pass

def add_entry(client,uid, entry):
    print(type(entry))
    if (len(entry)==0):
        return 0
    client["forgus"][get_location(client, uid)].insert_many(proc_entry(entry))

###############################################################################
########################### LOCATION ACESS FUNCTIONS ##########################
###############################################################################

def get_last_entry(client, location, num):
    return(list(client["forgus"][location].find({},{"_id":False}).sort("time",pymongo.DESCENDING).limit(num)))

def get_entry_by_date(client, location, startdate, enddate):
    start = datetime.datetime.strptime(startdate, "%Y-%m-%dT%H:%M:%S")
    end = datetime.datetime.strptime(enddate, "%Y-%m-%dT%H:%M:%S")
    print(start)
    print(end)
    print(type(start))
    print(list(client["forgus"][location].find({'time': {'$gte': start, '$lt': end}}, {"_id":False})))
    return(list(client["forgus"][location].find({'time': {'$gte': start, '$lt': end}}, {"_id":False})))

def get_all_entry(client):
    res = {}
    for i in client["forgus"].collection_names():
        if i=="devices" or i=="system.indexes":
            pass
        else:
            res[i] = list(client["forgus"][i].find({}, {"_id":False}))
    return res
    #client["forgus"][location].find({}, {"time_stamp":False}

###############################################################################
########################### DEVICES ACESS FUNCTIONS ###########################
###############################################################################

def get_location(client, uid):
    print(uid)
    print(client["forgus"]["devices"].find_one({"uid":uid})["location"])
    return client["forgus"]["devices"].find_one({"uid":uid})["location"]

def get_uid(client, location):
    print(location)
    return client["forgus"]["devices"].find_one({"location":location})["uid"]

def get_key(client, uid):
    return client["forgus"]["devices"].find_one({"uid":uid})["key"]

def get_all_device(client):
    return list(client["forgus"]["devices"].find({}, {"_id":False, "key":False}))

###############################################################################
########################### DATABASE INITALIZATION ############################
###############################################################################

def gen_locations(num):
    locations = []
    # entry["uid"] = "123456789"c
    # entry["location"] = "loc1"
    # entry["coord"] = [37.673311, -121.907643]

    uid = 123456789
    locationz = "loc"
    coordz = [37.673311, -121.907643]
    location=locationz
    coord = coordz
    #coordz = [[37.69473391756284, -122.8945729783403], [37.703280406206495, -121.88815547216618], [37.685923924402374, -121.88722497530328], [37.69026352844625, -121.8880059689976], [37.697110805524154, -121.88550204594762], [37.70269225528533, -121.88776822392856], [37.68578939413647, -121.8945117033698], [37.689149968133094, -121.88152837833326], [37.70095619481186, -121.88885856212539], [37.6999652266756, -121.89647833440817]]
    for i in range(num):
        locations.append({"uid":uid, "location":location, "coord":coord, "key":security.genkey()})
        uid = uid+1
        location = locationz + str(i)
        coord[0] = coordz[0]+random.uniform(0.01, 0.05)*(random.randint(-1,1))
        coord[1] = coordz[1]+random.uniform(0.01, 0.05)*(random.randint(-1,1))
    return locations

def gen_entries(num):
    entry = []
    d = datetime.timedelta(days = 1)
    for i in range(num):
        entry.append({"time":(datetime.datetime.now()-d).replace(microsecond=0).isoformat()})
    return entry

def init_db(client, locations, entries):
    #client.drop_database("forgus")
    #client["forgus"].create_collection("devices")
    #client["forgus"]["devices"].remove({})
    add_location(client, locations)

#    for i in client["forgus"].list_collection_names():
    for i in client["forgus"].collection_names():
        print(i)
        if i=="devices" or i=="system.indexes":
            pass
        else:
            add_entry(client, get_uid(client, i), entries)

###############################################################################
########################### MISC FUNCTIONS ####################################
###############################################################################

def proc_entry(entry):
    print(entry)
    proc = []
    print(type(entry))
    for i in entry:
        print(i)
        proc.append({"time":datetime.datetime.strptime(i["time"], "%Y-%m-%dT%H:%M:%S")})
    return proc

def export_collection(client, collection):
    os.system("mongoexport -d forgus -c "+str(collection)+" -o ./locations/"+str(collection)+"____"+str(str(datetime.datetime.today().strftime("%m%d%y")))+".json --jsonArray ")
    # theres a lot of other ways we can implement this; we'll see which one is better


def test():
    client = MongoClient()
    init_db(client, gen_locations(3), gen_entries(5))
    export_collection(client, "devices")
#    for i in client["forgus"].list_collection_names():
    for i in client["forgus"].collection_names():
        if i=="devices" or i=="system.indexes":
            pass
        else:
            export_collection(client, i)

def test1():
    client = MongoClient()
    add_entry(client, get_uid(client, "loc1"), gen_entries(5))
    a = get_entry_by_date(client, "loc1", "2021-03-01T00:04:49", "2021-03-01T10:09:49")
    print(a)

if __name__=="__main__":
    # get_all(MongoClient())
    test()

"""
Database Requirements

Things to keep track of:
- uid number/ID of device
- Location of device
- A log of all of the foot traffic of the location the device covers

Things that needs to be accessed:
- Foot traffic data by location
- Foot traffic data by time
- Status of devices by location/uid

Things that needs to be edited:
- Foot traffic data by location
- Foot traffic data by uid number/ID
- uid number by location
- Location by uid number

Database Schema

DB         COL        DOC
# forgus   < devices   < {"uid": uid number, "location": location, "active" : True, "coord":{longx, longy}, "key": symmetric_key}
#          < location  < {"date_stamp": datetime.datetime.utcnow(), "traffic":time as string}
                         {"date_stamp": datetime.datetime.utcnow(), "time":time as string}
"""
