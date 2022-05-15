import cv2
import os
import time
import requests
from PIL import Image, ImageDraw
import json
import base64
from datetime import datetime
from pymongo import MongoClient

def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция для обрезки изображения по центру.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


tyty = 0
url = "http://62.113.114.68:8006/object-to-json"

# for i in range(1,59):
#     os.mkdir(str("./result/"+str(i)))
cap = cv2.VideoCapture('dd.avi')
n = 0
nb = 0
kkb = 0
while True:
    ret, frame = cap.read()
    if cv2.cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif frame is None:
        break
    if n%21 == 0:
        #time.sleep(5)
        print(r"dd"+ str(n) +'.jpg')
        cv2.imwrite(r'result/'+'r' +str(n)+'.jpg',frame)
        #time.sleep(1)
        file = {'file': open(r'result/'+'r'+ str(n)+'.jpg', "rb")}
        resp = requests.post(url,files=file)
        if str(resp.text) != '{"result":[]}':
            print(resp.text)
            s = json.loads(str(resp.text))
            #print(s)
            gg = -1
            lllaaa = 0
            while True:
                gg = gg + 1
                if lllaaa == 0:
                    try:
                        if s['result'][gg]['name'] == "trashcan":
                            print("-------------")
                            print("")
                            print(s['result'][gg])
                            print("")
                            print("-------------")
                            lllaaa = 1
                            #print(type(s))
                            im = Image.open(r'result/'+'r' +str(n)+'.jpg')
                            (widthim, heightim) = im.size
                            print(widthim,heightim)
                            im = crop_center(im, widthim,heightim)
                            xmin = int(s["result"][gg]["xmin"])
                            ymin = int(s["result"][gg]["ymin"])
                            xmax = int(s["result"][gg]["xmax"])
                            ymax = int(s["result"][gg]["ymax"])
                            print(widthim/heightim)
                            print(heightim/widthim)
                            draw = ImageDraw.Draw(im)
                            draw.rectangle((xmin*2,ymin*2,xmax*2,ymax*2), outline="red",width=10)
                            print(im)
                            im.save(r'result/'+'r' +str(n)+'.jpg', quality=95)
                            with open(r'result/'+'r' +str(n)+'.jpg', "rb") as image_file:
                                str1 = base64.b64encode(im.read())
                            #print(resp.text)
                    except:
                        break;
                else:
                    break;
            typ = 0
            if str(s).count("garbage") >0:
                typ = "Негабаритный мусор"
                with open(r'result/'+'r' +str(n)+'.jpg', "rb") as image_file:
                    str1 = base64.b64encode(image_file.read())
            if str(s).count("big_garbage") >0:
                typ = "Негабаритный мусор"
                with open(r'result/'+'r' +str(n)+'.jpg', "rb") as image_file:
                    str1 = base64.b64encode(image_file.read())

            if typ == 0 and tyty == 1:
                tyty = 0

            if typ != 0 and tyty == 0:
                tyty = 1
                time = datetime.now()
                data = datetime.today().strftime('%d-%m-%y')
                time = time.strftime("%H:%M")
                address = "Краснодарская - Терская"
                coardinates = "44.89551372892196, 37.31729088054113"
                prev_datas = [0,0,0,0,0,0,0,0,0,0,0]
                with open(r'result/'+'r' +str(n)+'.jpg', "rb") as image_file:
                    prev = base64.b64encode(image_file.read())
                prev_datas[0] = prev

                client = MongoClient("45.10.42.122", 27017)
                #client = MongoClient("localhost", 27017)
                db = client.tasks
                kkb = kkb + 1

                data = {
                'taskNumber': kkb,
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



        #отправка картинок блоку ии

        #получение ответа от блока ии и занос полученной информации в бд

        #дальше работа бот
    n+=1

cap.release()
cv2.destroyAllWindows()