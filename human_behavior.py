
import argparse
import datetime
import imutils
import math
import cv2
import numpy as np
import serial 
#import mail_python as mail

width = 600

textIn = 0
textOut = 0

ser = serial.Serial('/dev/ttyUSB1',9600)


rec=cv2.createLBPHFaceRecognizer();
rec.load("trainer/trainer.yml")
id = 0
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,3,1,0,1)

def testIntersectionIn(x, y):

    res = -450 * x + 400 * y + 157500
    if((res >= -550) and  (res < 550)):
        print (str(res))
        return True
    return False



def testIntersectionOut(x, y):
    res = -450 * x + 400 * y + 180000
    if ((res >= -550) and (res <= 550)):
        print (str(res))
        return True

    return False

camera = cv2.VideoCapture(1)
thresholdValue = 180

firstFrame = None

# loop over the frames of the video
while True:
	
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    text = "Unoccupied"

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=width)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, thresholdValue, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # loop over the contours
    for c in cnts:
		
        # if the contour is too small, ignore it
		if cv2.contourArea(c) < 5000:
				continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		id,conf=rec.predict(gray[y:y+h,x:x+w])
		cv2.line(frame, (0, 50), (1000, 50), (250, 0, 1), 2) #blue line
		cv2.line(frame, (0, 400) ,(1000,400 ), (0, 0, 255), 2)#red line

		#if not (testIntersectionOut((x + x + w) / 2, (y + y + h) / 2)) or (testIntersectionIn((x + x + w) / 2, (y + y + h) / 2)):
		if(id == 9787):
			id="good gear"
			ser.write("G")
		else:
			id = "faulty"
			ser.write("S")	
		cv2.cv.PutText(cv2.cv.fromarray(frame),str(id), (x,y+h),font,255);	

		

		rectagleCenterPont = ((x + x + w) /2, (y + y + h) /2)
		cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)

		#if(testIntersectionIn((x + x + w) / 2, (y + y + h) / 2)) and (testIntersectionOut((x + x + w) / 2, (y + y + h) / 2)):
		#	textIn += 1
            

		#if(testIntersectionOut((x + x + w) / 2, (y + y + h) / 2)):
            
		#	textOut += 1
            

        # draw the text and timestamp on the frame

        # show the frame and record if the user presses a key
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)
		cv2.imshow("Security Feed", frame)
cv2.imshow("Thresh", thresh)
cv2.imshow("Frame Delta", frameDelta)
cv2.imshow("Security Feed", frame)
				
	
	



# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


	
