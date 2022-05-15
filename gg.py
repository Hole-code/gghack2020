import cv2
import os
import time
import requests
from PIL import Image, ImageDraw

print("ok1")
# for i in range(1,59):
#     os.mkdir(str("./result/"+str(i)))
cap = cv2.VideoCapture("dd.avi")
n = 0
print("ok2")

while True:
    print("ok3")
    ret, frame = cap.read()
    if cv2.cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif frame is None:
        break
    if n%21 == 0:
        print(r"dd"+ str(n) +'.jpg')
        cv2.imwrite(r'result/'+'r' +str(n)+'.jpg',frame)

        #отправка картинок блоку ии

        #получение ответа от блока ии и занос полученной информации в бд

        #дальше работа бот
        n+=1

cap.release()
cv2.destroyAllWindows()