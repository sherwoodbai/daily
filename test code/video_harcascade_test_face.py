import cv2
import numpy as np 
import sqlite3
import os

conn = sqlite3.connect('database.db')
if not os.path.exists('./dataset'):
    os.makedirs('./dataset')
c = conn.cursor()
c.execute('Create Table users(name text not null)')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture("rtsp://110.102.1.19:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream")
uname = input("Enter your name: ")
c.execute('INSERT INTO users(name) VALUES (?)', (uname,))
uid = c.lastrowid
sampleNum = 0

while True:
  ret, img = cap.read()
  
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  #faces = face_cascade.detectMultiScale(img, 1.3, 5)
  for (x,y,w,h) in faces:
    sampleNum = sampleNum+1
    cv2.imwrite("dataset/User."+str(uid)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
    #cv2.waitKey(100)
  cv2.imshow('img',img)
  
  k = cv2.waitKey(0)
  if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
   
    
cap.release()
conn.commit()
conn.close()
cv2.destroyAllWindows()
