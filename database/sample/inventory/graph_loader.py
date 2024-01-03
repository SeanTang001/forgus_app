from matplotlib import pyplot as pp
from pymongo import MongoClient
import json
import pprint
import numpy as np
import datetime

client = MongoClient()
walmart = list(client["inventory"]["walmart"].find({}))
target = list(client["inventory"]["target"].find({}))
safeway = list(client["inventory"]["safeway"].find({}))

def gendates():
    s = datetime.datetime.now().day - 5
    client["inventory"]["walmart"].update_many({}, {"$set":{"past":[]}})
    client["inventory"]["safeway"].update_many({}, {"$set":{"past":[]}})
    client["inventory"]["target"].update_many({}, {"$set":{"past":[]}})
    
    for i in range(5):
        client["inventory"]["walmart"].update_many({}, {"$addToSet":{"past":{datetime.datetime(2020, 10, s+i).strftime("%x"):0}}}) 
        client["inventory"]["safeway"].update_many({}, {"$addToSet":{"past":{datetime.datetime(2020, 10, s+i).strftime("%x"):0}}})
        client["inventory"]["target"].update_many({}, {"$addToSet":{"past":{datetime.datetime(2020, 10, s+i).strftime("%x"):0}}})


def addDate():
    res = findAverage()
    for a in list(res.keys()):
        for b in list(res[a].keys()):
            client["inventory"][a].update({"address":b}, {"$addToSet":{"past":{datetime.datetime.now().strftime("%x"):res[a][b]}}})

def findAverage():
    t = {"walmart":walmart, "safeway":safeway, "target":target}
    #t = {"target":target}
    res ={}
    for a in list(t.keys()):
        b = t[a]
        temp = {}
        for i in b:
            ttl = 0
            for x in list(i.keys()):
                if x == "address" or x == "_id" or x == "past":
                    continue
                try:
                    ttl = ttl + i[x]["score"]
                except:
                    print i[x]
                    print x
                    print a
                    print i[x]["score"]
                    pass
            temp[i["address"]] = ttl/17
        res[a] = temp
    return res

# def makeTrendGraph():
# #type of goods : time vs score overall
# #type of goods : time vs score by stores
# #type of goods vs score overall

def makeStoreGraph():
#time vs total score
#item vs item score
    stores = ["walmart", "safeway", "target"]
    for i in stores:
        address = list(client["inventory"][i].find({}))
        for v in address:
            addresz = v["address"]
            print addresz.replace(" ", "_")
            print v["_id"]
            #print(v["address"])
            #print(v.values()[0]["score"])
            #print len(v["past"])

            #print ([a.keys()[0] for a in v["past"][(len(v["past"])-5):]])
            
            pp.rcParams["figure.figsize"] = (7,3)
            fig, axe = pp.subplots(1,2)
            #print axe
            xticks = [a.keys()[0] for a in v["past"][(len(v["past"])-5):]]
            axe[0].plot(range(5), [a.values()[0] for a in v["past"][(len(v["past"])-5):]])
            axe[0].set_xticks(range(5))
            axe[0].set_xticklabels(xticks, rotation = 90)
            axe[0].title.set_text("historic trend")
            axe[0].tick_params(axis='both', which='minor', labelsize=8)
            del(v["past"]) 
            del(v["address"])
            del(v["_id"])

            #pprint.pprint([x["score"] for x in v.values()])
            #pprint.pprint([v.keys()])
            axe[1].bar(range(len(v.keys())), [x["score"] for x in v.values()])
            axe[1].set_xticks(range(len(v.keys())))
            xticks = v.keys()
            axe[1].set_xticklabels(xticks, rotation = 90)
            axe[1].title.set_text("availability of goods")
            # axe[1].tick_params(axis='both', which='minor', labelsize=8)
            a1 = axe[1].twinx()
            a1.plot(range(len(v.keys())), [10 for z in range(len(v.keys()))], "r")
            pp.tight_layout()
            fig.savefig("../../FlaskApp/static/"+i+"/"+addresz.replace(" ", "_")+".png", bbox_inches="tight")
            pp.close()

def graph_load():
    makeStoreGraph()

# pprint.pprint(average_finder())

#what data do people want to see?
#perhaps ... change in supply for different stores over time
#IDEAS:

#Average score of different things across different stores - bar /
#Average price of different things across different stores - bar
#
#Location Analysis?(?)
#supply over time trend - plot
#price over time trend - plot
#
#supply over time based on county- bar
#supply over time based on shop type - bar
#supply over time based on over general - bar
#
#to simplify process, everything will happen at day-day interval
#
#persistent storage of score across different days
#schema: date - {address:address, old scores : {date:time}}