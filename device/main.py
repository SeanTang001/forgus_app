import time, analog_sonic, analog_ir, json, phone, threading, datetime, requests, jwt, internet, requests

apiz = requests.session()
config = json.loads(open("./config.json","r").read())
res = {"data":[], "info":{"location":config["location"], "uid":config["phone"], "coord":config["coord"]}}

def phone_feedback():
    global res
    while True:
        time.sleep(5)
        print("sending")
        print(res)
        phone.send_msg(json.dumps(res)+"^>", '"'+"+"+config["phone"]+'"')
        res["data"]=[]

def internet_feedback(key):
    global res
    while True:
        time.sleep(10)
        print("sending")
        print(res)
        internet.add_entry(apiz, key, res["data"])
        res["data"]=[]
        
def sensors():
    global res
    while True:
        print("checking")
        print(res)
        time.sleep(5)
        if (analog_ir.isHuman()):
	        res["data"].append({"time":datetime.datetime.now().replace(microsecond=0).isoformat()})

def main():
    if config["comm"] == "phone": 
        pf = threading.Thread(target=phone_feedback)
    else:
        key = internet.add_device(apiz)
        pf = threading.Thread(target=internet_feedback, args=(key,))
    s = threading.Thread(target=sensors, args=())
    pf.start()
    s.start()
    #pf.join()
    #s.join()

if __name__ == "__main__":
    main()
