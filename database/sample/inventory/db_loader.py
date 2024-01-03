import target, walmart, safeway
import requests
import pprint
import time
import json
import multiprocessing
import threading
from pymongo import MongoClient
from fake_useragent import UserAgent

items = json.load(open("../jsons/item.json"))
targetId = json.load(open("../jsons/target_id.json"))
walmartId = json.load(open("../jsons/walmart_id.json"))
safewayId = json.load(open("../jsons/safeway_id.json"))
tcin = json.load(open("../jsons/tcin.json"))
pp = pprint.PrettyPrinter(indent=2)
ts = time.time()
maindict = {}
client = MongoClient()


def parse_by_type(maindict):
	for i in maindict.keys():
		for a in maindict[i]:
			try:
				del[a["_id"]]
			except:
				pass
			if not (client["inventory"][i].update({"address":a["address"]}, {"$set":a})["updatedExisting"]):
				client["inventory"][i].insert_many(maindict[i])
				break

def parse_by_store(maindict):
	res = {"walmart":{}, "safeway":{}, "target":{}}
	resx = {"walmart":[], "safeway":[], "target":[]}
	for a in maindict.keys():
		for b in maindict[a]:
			try:
				res[b["type"]][b["address"]][a] = {"items":b["items"], "score":b["summaryTotal"]["quantityRank"]}
			except:
				res[b["type"]][b["address"]] = {}
				res[b["type"]][b["address"]][a] = {"items":b["items"], "score":b["summaryTotal"]["quantityRank"]}

	for x in res.keys():
		for z in res[x].keys():
			resx[x].append({"address":z})
			for i in res[x][z].keys():
				resx[x][len(resx[x])-1][i] = res[x][z][i]

	for i in resx.keys():
		for a in resx[i]:
			try:
				del[a["_id"]]
			except:
				pass
			if not (client["inventory"][i].update({"address":a["address"]}, {"$set":a})["updatedExisting"]):
				client["inventory"][i].insert_many(resx[i])
				break

def db_load(res):
	parse_by_store(res)
	parse_by_type(res)
	print("[+]db done loading")
