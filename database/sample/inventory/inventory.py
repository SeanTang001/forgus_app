import target, walmart, safeway
import requests
import pprint
import time
import json
import multiprocessing
import threading
from fake_useragent import UserAgent

items = json.load(open("../jsons/item.json"))
targetId = json.load(open("../jsons/target_id.json"))
walmartId = json.load(open("../jsons/walmart_id.json"))
safewayId = json.load(open("../jsons/safeway_id.json"))
tcin = json.load(open("../jsons/tcin.json"))
pp = pprint.PrettyPrinter(indent=2)
ts = time.time()
maindict = {}

def walmart_search(maindict):
	for i in items:
		for x in list(walmartId.keys()):
			res = walmart.searchquery(i, x, walmartId[x][2], 10)
			if (res!=None):
				maindict[i].append(res)
			else:
				pass

def target_search(maindict):
	for i in items:
		for x in list(targetId.keys()):
			res = target.searchquery(i,tcin[i],x,targetId[x][0])
			if (res!=None):
				maindict[i].append(res)
			else:
				pass

def safeway_search(maindict):
	for i in items:
		for x in list(safewayId.keys()):
			res = safeway.searchquery(i,x,safewayId[x][0])
			if (res!=None):
				maindict[i].append(res)
			else:
				pass

def main():
	for i in items:
		maindict[i] = []
	w = threading.Thread(target=walmart_search, args=(maindict, ))
	w.start()
	t = threading.Thread(target=target_search, args=(maindict, ))
	t.start()
	s = threading.Thread(target=safeway_search, args=(maindict, ))
	s.start()
	s.join()
	w.join()
	t.join()
	print(time.time()-ts) 
	return maindict

def anaylsis():
	res = json.load(open("../jsons/res.json"))
	a = res.keys()
	maindict = {}
	for i in a:
		maindict[i] = {"walmart":0, "target":0, "safeway":0}
		g = res[i]
		for x in g:
			if (x["items"]==[]):
				maindict[i][x["type"]]=maindict[i][x["type"]]+1
	return maindict

def test():
	x = open("../jsons/res.json", "w")
	x.write(json.dumps(main(), indent=2))
	x.close()

if __name__ == "__main__":
	test()
	print(anaylsis())