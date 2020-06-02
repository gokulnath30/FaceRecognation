import cv2, os
from datetime import date
from datetime import datetime 


today = date.today()
source = 'Source'  
date_file = str(today) 
path = os.path.join(source, date_file)

if not os.path.isdir(path): 
    os.mkdir(path) 
    
(width, height) = (130,150)    
face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml') 
# webcam1 = cv2.VideoCapture(0)    
count = 1 

while True:
    # webcam = webcam1
    webcam = cv2.VideoCapture("rtsp://admin:P@ssw0rd@192.168.168.150:554")   
    (ret, frame) = webcam.read() 
    frame_size=cv2.resize(frame, (1000, 600)) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    
    for (x, y, w, h) in faces: 
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        pic_name=str(count)
        
        cv2.imwrite('%s/%s.png' % (path,pic_name), face_resize) 
        count += 1 
        print(date_file)
        
    #cv2.imshow('Camera', frame_size)
    key = cv2.waitKey(30) 
    if key == 27:
        break




    
  
