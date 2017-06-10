
import serial
import numpy as np
import cv2

cam=cv2.VideoCapture(0)
FaceDetect= cv2.CascadeClassifier('gear.xml')


cam.set(3,400)
cam.set(4,400)


ser = serial.Serial('/dev/ttyUSB0',9600)
rec=cv2.createLBPHFaceRecognizer();
rec.load("trainer/trainer.yml")
id=0
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,3,1,0,1)
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = FaceDetect.detectMultiScale(gray, 1.3, 5)
    if(len(faces)!=0):
        for (x,y,w,h) in faces :
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				id,conf=rec.predict(gray[y:y+h,x:x+w])
				if(id == 9787):
					id="nikhilesh"
					ser.write("G")
				if (id == 46):
					id = "pratik"
					ser.write("S")	
				cv2.cv.PutText(cv2.cv.fromarray(img),str(id), (x,y+h),font,255);	
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

