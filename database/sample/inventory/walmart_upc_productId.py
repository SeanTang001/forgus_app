import requests
import walmart
import pprint
import time
import json
import bs4
import re
from fake_useragent import UserAgent
import pycurl
import io

maindict = {}
ua = UserAgent()

def parse(l):
    for i in range(len(l["searchContent"]["preso"]["items"])):
        try:
            maindict[l["searchContent"]["preso"]["items"][i]["usItemId"]] = l["searchContent"]["preso"]["items"][i]["upc"][2:]+walmart.upcchecksum(l["searchContent"]["preso"]["items"][i]["upc"][2:])
        except:
            pass
    pages = l["searchContent"]["preso"]["pagination"]
    return len(pages["pages"])+1

# <script id="searchContent" type="application/json">
# searchContent, preso, items, usItemId, upc




def byname():
    item = json.load(open("../jsons/item.json"))
    for i in item:
        print i 
        x = requests.get("https://www.walmart.com/search/?query="+i+"")
        page = bs4.BeautifulSoup(x.text, features="html.parser")
        l = json.loads(page.find('script', id = 'searchContent', type='application/json').text)
        for x in range(2, parse(l)+1):
            x = requests.get("https://www.walmart.com/search/?query="+i+"&page="+str(x)+"")
            page = bs4.BeautifulSoup(x.text, features="html.parser")
            l = json.loads(page.find('script', id = 'searchContent', type='application/json').text)
            parse(l)

def byid():
    ids = json.load(open("../jsons/res2.json"))
    temp = []
    for i in range(len(ids)):
        print i
        x = requests.get("https://www.walmart.com/search/?query="+ids[i]+"")
        page = bs4.BeautifulSoup(x.text, features="html.parser")
        l = json.loads(page.find('script', id = 'searchContent', type='application/json').text)["searchContent"]["preso"]["items"]
        for a in l:
            g = a["productPageUrl"]
            print g
            x = requests.get("https://walmart.com"+g)
            page = bs4.BeautifulSoup(x.text, features="html.parser")
            l = json.loads(page.find('script', id = 'item', type='application/json').text)
            temp.append(l)
    json.dump(temp, open("../jsons/res4.json","w"))
 

byid()
res = json.load(open("../jsons/res4.json", "r"))
for i in res:
    maindict[i["item"]["product"]["buyBox"]["products"][0]["usItemId"]] = i["item"]["product"]["buyBox"]["products"][0]["upc"]
res = open("../jsons/res4.json", "w")
res.write(json.dumps(maindict, indent=2))
res.close()    


# k = open("res4.json", "r").read()
# x = r"\"upc\"\:(.*?)\,"
# res = open("res4.json", "w")
# res.write(json.dumps(re.findall(x, k), indent=2))
# res.close()    
