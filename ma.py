import cv2
import os
import time
import requests
from PIL import Image, ImageDraw
import json
import base64
from datetime import datetime
from pymongo import MongoClient

with open(r'result/'+'r' +str(189)+'.jpg', "rb") as image_file:
    str1 = base64.b64encode(image_file.read())

time = datetime.now()
data = datetime.today().strftime('%d-%m-%y')
time = time.strftime("%H:%M")
address = "Краснодарская - Терская"
coardinates = "44.89551372892196, 37.31729088054113"
prev_datas = [0,0,0,0,0,0,0,0,0,0,0]
with open(r'result/'+'r' +str(189)+'.jpg', "rb") as image_file:
    prev = base64.b64encode(image_file.read())
prev_datas[0] = prev

client = MongoClient("45.10.42.122", 27017)
#client = MongoClient("localhost", 27017)
db = client.tasks
typ = "Негабаритный мусор"

data = {
'taskNumber': "1",
'photos': [str1,str1],
'video':str1,
'description': typ,
'date':data,
'time':time,
'adress': address,
'coordinates': coardinates,
'camera_id': '34'
}

db.general.insert_one(data)
print("GAGAGA")