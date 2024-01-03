from matplotlib import pyplot as pp
from pymongo import MongoClient
import json
import csv
import pprint
import numpy as np
import datetime

client = MongoClient()
walmart = list(client["inventory"]["walmart"].find({}, {"_id": 0 }))
target = list(client["inventory"]["target"].find({}, {"_id": 0 }))
safeway = list(client["inventory"]["safeway"].find({}, {"_id": 0 }))

def csv_write(obj, name, csv_writer, count):
    header = ["type", "address", "item type", "score", "stauts", "name", "price", "upc"]
    csv_writer.writerow(header)
    count = 1

    for i in obj:
        for x in i.keys():
            if x == "_id" or x=="address" or x=="past":
                continue
            csv_writer.writerow([name, i["address"], x, i[x]["score"],"","", "", ""])
            for g in i[x]["items"]:
                try:
                    row = ["","","", "",g["status"], g["name"], g["price"], g["upc"]]
                except:
                    row = ["","","", "",g["status"], g["name"], g["price"], 0]
                csv_writer.writerow(row)


def download_load():
    x = open("../../FlaskApp/static/data.json", "w")
    x.write(json.dumps({"walmart":walmart,"target":walmart,"safeway":walmart}))

    x = open("../../FlaskApp/static/data.csv", "w")
    csv_writer = csv.writer(x)

    csv_write(walmart, "walmart", csv_writer, 0)
    csv_write(walmart, "target", csv_writer, 1)
    csv_write(walmart, "safeway", csv_writer, 1)


#type of goods : time vs score overall
#type of goods : time vs score by stores
#type of goods vs score overall

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