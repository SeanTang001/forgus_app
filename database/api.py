import json, time
from pymongo import MongoClient

from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Response, WebSocket, Security, Depends
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

import pickle
import os.path
import hashlib

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
# from jose import JWTError, jwt

import db_loader, security

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="getToken", scopes={"Student":"student_access", "Teacher":"teacher_access", "Admin":"admin_access", "device":"device_access"})

key = "554a2501bd350409fadb7390e7f4b8622350d94324747278e434e083442e7438"
#which algo to use?
algo = "HS256"
expire_time = 1
emergency = False
broadcast_list = {}

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient()

###############################################################################
##################### DATABASE ACCESS ENDPOINTS ###############################
###############################################################################

@app.get("/a/{location}/{num}")
async def getEntryByIndex(request: Request, location:str, num:str):
    return {"data":db_loader.get_last_entry(client, location, int(num))}

@app.get("/d/{location}/{startdate}/{enddate}")
async def getEntryByDateAndTime(request: Request, location:str, startdate:str, enddate:str):
    return {"data":db_loader.get_entry_by_date(client, location, startdate, enddate)}

@app.get("/e")
async def getAllDevice(request: Request):
    return {"data":db_loader.get_all_device(client)}

@app.get("/f")
async def getAllEntry(request: Request):
    return {"data":db_loader.get_all_entry(client)}


###############################################################################
##################### DATABASE ENTRY ENDPOINTS ################################
###############################################################################

@app.get("/b/{uid}/{payload}")
async def addentry(request: Request, payload:str, uid:str):
    entry = security.decrypt(db_loader.get_key(client, uid), payload)
    db_loader.add_entry(client, uid, json.loads(entry))

#authenticate at first using a manual login -- too much work, and not very reliable -- generate config files to copy paste?

@app.post("/c/{uid}/{payload}")
async def addpayload(request: Request, payload:str, uid:str):
    formz = await request.form()
    pwd = dict(formz)["password"]
    print(pwd)
    print(getpassword())
    m = hashlib.sha256()
    m.update(pwd.encode())
    pl = json.loads(payload)
    if m.hexdigest() == getpassword():
        pl["key"] = security.genkey()
        db_loader.add_location(client, [pl])
        return db_loader.get_key(client, uid)

###############################################################################
########################### API SECURITY FUNCTIONS ############################
###############################################################################
def getpassword():
    m = hashlib.sha256()
    m.update('password'.encode())
    return m.hexdigest()
