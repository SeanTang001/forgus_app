import emai_user, db_loader, json, pymongo, time
from pymongo import MongoClient

config = json.load(open("./config.json"))

rec_server = emai_user.rec_conn_init(config["email_cred"])
client = MongoClient()

while True:
    time.sleep(5)
    print("[+] checking email")
    res = emai_user.mail_checker(rec_server)
    print(res)
    for i in res:
        print("jjj")
        print(i)
        key = db_loader.add_location(client, [i["info"]])
        if (len(i["data"])!=0):
            db_loader.add_entry(client, i["info"]["uid"], i["data"])

        # def add_entry(client,uid, entry):
        #     print(type(entry))
        #     if (len(entry)==0):
        #         return 0
        #     client["forgus"][get_location(client, uid)].insert_many(proc_entry(entry))