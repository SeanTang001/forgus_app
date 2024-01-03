import json, time
from pymongo import MongoClient

from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Response, WebSocket, Security, Depends
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://127.0.0.1:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = MongoClient()

@app.get("/a/{category}")
async def getInventoryByCategory(request: Request, category:str):
    data = client["inventory"][category].find({},{"_id":False})
    #pprint.pprint(list(data))
    return {"data":list(data)}

@app.get("/b/{category}/{address}")
async def getInventoryByCategoryAdress(category:str, address:str):
    data = client["inventory"][category].find({"address":address},{"_id":False})
    return {"data":list(data)}
