from pymongo import MongoClient

client = MongoClient("45.10.42.122", 27017)
#client = MongoClient("localhost", 27017)
db = client.tasks

data = {
    'taskNumber': '',
    'photos': ['Base64','Base64'],
    'video':'',
    'description': '',
    'date':'20.04.2021',
    'time':'15:40',
    'adress': '',
    'coordinates': ''
}

data1 = {
    'taskNumber': '',
    'photos': ['Base64','Base64'],
    'video':'',
    'description': '',
    'date':'20.04.2021',
    'time':'15:40',
    'adress': '',
    'coordinates': ''
}


db.general.insert_one(data1)
# camera10tasks = db.general.find({'camera_id':'10'})

# for camera10task in camera10tasks:
#     print(camera10tasks)
#     break
# for item in db.general.find():
#     if item['camera_id']:
#         print(item['camera_id'])



#user.photo,user.description,user.date,user.time,user.adress,user.url


