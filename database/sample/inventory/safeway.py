import requests
import pprint
import time
import json
from fake_useragent import UserAgent


def get_id():
    zip = json.load(open(".../jsons/zips.json"))
    maindict = {}
    for i in zip:
        x = json.loads(requests.get("https://www.safeway.com/abs/pub/xapi/storeresolver/all?zipcode="+i+"&radius=50&size=10").text)
        try:
            for k in range(x["instore"]["count"]):
                maindict[x["instore"]["stores"][k]["locationId"]] = [x["instore"]["stores"][k]["address"]["line1"], x["instore"]["stores"][k]["address"]["city"]]
        except:
            pass
    res = open("../jsons/safeway_id.json", "w")
    res.write(json.dumps(maindict, indent=2))
    res.close()

def searchquery(itemtype, storeId, address):
    print("type: safeway id: "+storeId+"	itemtype: "+itemtype)
    item = itemtype.replace("-", " ")
    if (item=="Bottled Water"):
        item = "water"
    res = {}
    res["type"] = "safeway"
    res["storeId"] = storeId
    res["address"] = address
    res["items"] = []
    x = json.loads(requests.get("https://suggest.dxpapi.com/api/v1/suggest/?account_id=6175&domain_key=albertsons&url=www.safeway.com&ref_url=www.safeway.com&q="+item+"&request_type=suggest&view_id="+storeId+"").text)
    try:
        for i in x["response"]["products"]:
            res["items"].append({"status": "In Stock", 
                "price": i["sale_price"], 
                "name": i["title"],
                "upc": i["upc"]})
    except:
        return None
    if (len(res["items"])==0):
        return None
    res["summaryTotal"] = {"quantityRank":10*float(len(res["items"]))/8}
    res["items"] = res["items"][:5]
    return res

def safeway(filename):
    t = time.time()
    maindict = {}
    storeId = json.load(open("../jsons/safeway_id.json"))
    storeId = {"1476": [
    "1300 W San Carlos St", 
    "San Jose"
  ]}
    items = json.load(open("../jsons/item.json"))
    for i in items:
        maindict[i] = []
        for x in storeId.keys():
            res = searchquery(i, x, storeId[x][0])
            if res == None:
                continue
            maindict[i].append(res)
    res = open(filename, "w")
    res.write(json.dumps(maindict, indent=2))
    res.close()
    return maindict

if __name__ == "__main__":
    safeway("res2.json")