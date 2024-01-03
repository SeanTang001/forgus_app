

import time, datetime, requests, json, geocoder, security

config = json.loads(open("./config.json","r").read())
uid=config["phone"]
location =config["location"]
password = config["password"]
key = 0


server = config["server"]

def add_entry(api,key, res):
    api.get(server+"b/"+uid+"/"+security.encrypt(key, json.dumps(res))+" ")

def add_device(api):
    locations = {"uid":uid, "location":location, "coord":get_location()}
    x = api.post(server+"c/"+uid+"/"+json.dumps(locations)+"", data={"password":password})
    return x.text

def get_location():
    g = geocoder.ip('me')
    return(g.latlng)

def main():
    api = requests.session()
    key = add_device(api)
    add_entry(api, key, [{"time":datetime.datetime.today().replace(microsecond=0).isoformat()}])

if __name__ == "__main__":
    main()
