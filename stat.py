import matplotlib.pyplot as plt
import numpy as np
import json
from pymongo import MongoClient
import base64

client = MongoClient("45.10.42.122", 27017)
#client = MongoClient("localhost", 27017)
db = client.tasks
ww = db.stats2.find()[0]["photo"]
print(ww)


ww = int(db.workers.find()[0]["count"])
cc = int(db.cars.find()[0]["count"])
ff = int(db.fail.find()[0]["count"])







plt.title('Статистика задач по уборке')
index = ["Дворники","Машины","Ложные"]
values = [ww,cc,ff]
plt.bar(index,values,color="#5B42FE")
plt.tight_layout()
plt.savefig("stat.png")

with open(r'stat'+".png", "rb") as image_file:
	str1 = base64.b64encode(image_file.read())
db.stats2.update_one({'photo':{'$exists':'true'}},{'$set':{'photo':str1}} )


