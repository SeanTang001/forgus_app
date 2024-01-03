import os
import time
import db_loader, inventory, graph_loader, download_loader
import json
from pymongo import MongoClient
#run ../inventory/load_db every 1 hr

counter = 24
first_time = False

client = MongoClient()

#res = json.load(open("../jsons/res1.json"))
# db_loader.db_load(res)

#graph_loader.gendates()

if len(list(client["inventory"]["walmart"].find({}))) == 0:
    first_time =True


while True:
    res = inventory.main()
    x = open("../jsons/res1.json", "w")
    x.write(json.dumps(res))
    x.close()
    db_loader.db_load(res)
    download_loader.download_load()

    if (counter == 24):
        if first_time:
            graph_loader.gendates()
        graph_loader.addDate()
        counter = 0

    graph_loader.graph_load()

    counter = counter + 1
    time.sleep(60*60)
# Schedules job_function to be run once each minute

