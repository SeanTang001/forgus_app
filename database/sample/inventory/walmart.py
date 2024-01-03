import requests
import pprint
import time
import json
from fake_useragent import UserAgent

r = requests.Session()
ua = UserAgent()
pp = pprint.PrettyPrinter(indent=2)


id_upc = json.load(open("../jsons/id_upc.json"))
# id_upc = {"s":"s"}
# g = open("upc.json", "r")
# #x = requests.get("https://www.walmart.com/store/finder?location=95127&distance=100")
# #page = bs4.BeautifulSoup(x.text, features="html.parser")
# #l = json.loads(page.find('script', id = 'storeFinder', type='application/json').text)
# l = json.loads(g.read())
# #g.write(json.dumps(l, indent=4)) 
# #g.close()
# for i in range(len(l["storeFinder"]["storeFinderCarousel"]["stores"])):
#     print(l["storeFinder"]["storeFinderCarousel"]["stores"][i]["id"])
# #print(l["storeFinder"]["storeFinderCarousel"]["stores"][])
# g.close()


# {
#   city: {
#     store: {
#       address: address,
#       itemtype: {
#         summaryTotal: {
#           quantityRank: rank,
#           status: status,
#         },
#         items:[{itemname:itemname
#           price: price, 
#           status: status
#         }]
#       }
#     }
#   }
# }

corrected_price = {}
catid = {
	"Hand-sanitizer":"1005862_9011420",
    "Masks":"0",
    "Canned-Food":"976759",
    "Chicken":"0",
    "Beans":"0",
    "Pasta":"0",
    "Peanut-Butter":"0",
    "Bottled-Water":"0",
    "Rice":"0",
    "Hot-Dogs":"0",
    "Milk":"0",
    "Frozen-Foods":"976759_976791",
    "Toilet-Paper":"0",
    "Paper-Towels":"0",
    "Wet-Wipes":"0",
    "Meat":"0",
    "Bread":"0",
    "Egg":"0"}

def get(x):
	# c = pycurl.Curl()
	# buffer = io.BytesIO()
	# c.setopt(c.URL, x)
	# c.setopt(c.WRITEFUNCTION, buffer.write)
	# c.perform()
	# c.close()
	# return buffer.getvalue().decode('UTF-8')
	r.headers = {'User-Agent': ua.random}
	return r.get(x).text


def sortz(res):
	return sorted(res, key=lambda x: x["status"])[:5]

def upcchecksum(upc):
	upc = str(upc)
	if(len(upc)==11):
		pass
	if(len(upc)==10):
		upc = str(0)+upc
	if (len(upc)==12):
		return upc
	odd = 0
	even = 0
	for i in range(0, len(upc)):
		if ((i+1)%2==0):
			even = even + int(upc[i])
		else:
			odd = odd + int(upc[i])
	return upc+str(10-(((odd*3)+even)%10))
	

def score(items, instock, limitedstock):
	if (items==0):
		return 0
	x = 10/float(items)*instock + 10/float(items)*limitedstock
	return x


def searchquery(itemtype, storeId, address, size):
	if (itemtype=="Toilet-Paper" or itemtype=="Paper-Towels"):
		size = 5
	print("type: walmart id: "+storeId+"	itemtype: "+itemtype)
	x = json.loads(get("http://search.mobile.walmart.com/search?query="+itemtype+"&store="+str(storeId)+"&size="+str(size)+"&offset=00&cat_id="+str(catid[itemtype])+""))
	instock =0
	limitedstock = 0
	res = []
	itemType = {}
	ofs = 0
	for i in range(len(x["results"])):
		name = x["results"][i]["name"]
		try:
			status = x["results"][i]["inventory"]["status"]
		except:
			status = -1
		try:
			upc = str(x["results"][i]["productId"]["upc"])
		except:
			upc = -1
		try:
			price = x["results"][i]["price"]["priceInCents"]
		except:
			price = -1
		if (upc==-1):
			try:
				upc = id_upc[x["results"][i]["productId"]["WWWItemId"]]
			except:
				upc = -1
		if((price ==-1 and status == -1) and (upc!=-1)):
			price, status = statquery(str(upc), storeId)
		if((status == -1) and (upc!=-1)):
			price, status = statquery(str(upc), storeId)
		if((price ==-1) and (upc!=-1)):
			price= pricequery(str(upc), storeId)

		if("In Stock" in str(status)):
			instock = instock+1
		if ("Limited Stock" in str(status)):
			limitedstock = limitedstock+0.5
		if ("Out of Stock" in str(status)):
			continue
		if ("Unknown" in str(status) or status == -1):
			continue

		res.append({"name":name, "upc":upc, "price":price/100, "status":status})
	if (len(res)==0):
		return None
	res = sortz(res)
	itemType["items"] = res
	itemType["summaryTotal"] = {"quantityRank":score(len(res)+ofs, instock, limitedstock)}
	itemType["type"] = "walmart"
	itemType["address"] = address
	itemType["storeId"] = storeId
	return itemType


def pricequery(upc, idz):
	try:
		return corrected_price[upc]
	except:
		pass
	res = get("https://search.mobile.walmart.com/v1/products-by-code/UPC/"+upcchecksum(upc)+"?storeId="+idz+"")
	x = json.loads(res)
	try:
		price = x["data"]["inStore"]["price"]["priceInCents"]
	except:
		price = -1
	corrected_price[upc] = price
	print("upc: "+upc+" corrected price: "+str(price))
	return price

def statquery(upc, idz):
	res = get("https://search.mobile.walmart.com/v1/products-by-code/UPC/"+upcchecksum(upc)+"?storeId="+idz+"")
	x = json.loads(res)
	try:
		status = x["data"]["inStore"]["inventory"]["status"]
	except:
		status = "Unknown"
	try:
		price = x["data"]["inStore"]["price"]["priceInCents"]
	except:
		price = -1
	print("upc: "+upc+" corrected status: "+str(status))
	print("upc: "+upc+" corrected price: "+str(price))
	return price, status 

def walmart(filename):
	size = 10
	t = time.time()
	cities = json.load(open("../jsons/walmart_id.json"))
	items = json.load(open("../jsons/item.json"))
	#city = json.load(open("../jsons/city.json"))
	items = ["Hand-sanitizer"]
	cities = {"1789": ["Lodi", "Walmart Supercenter ", "1601 S Lower Sacramento Rd"]}
	maindict = {}
	a = list(cities.keys())
	for i in range(len(a)):
		maindict[cities[a[i]][0]] = {}
	for i in range(len(a)):
		maindict[cities[a[i]][0]][a[i].replace("#","")] = {"address":cities[a[i]][2]}
		for x in range(len(items)):
			res = searchquery(items[x], a[i].replace("#",""), cities[a[i]][2], size)
			if (res!=None):
				maindict[cities[a[i]][0]][a[i].replace("#","")][items[x]] = res
	pp.pprint(maindict)
	x = open(filename, "w")
	x.write(json.dumps(maindict, indent=2))
	x.close()
	print(time.time()-t)
	return maindict

if __name__ == "__main__":
	walmart("res3.json")