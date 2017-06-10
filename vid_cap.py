
import argparse
import datetime
import imutils
import math
import cv2
import numpy as np
import serial
width = 800

textIn = 0
textOut = 0

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

sampleNum = 0
camera = cv2.VideoCapture(0)
#ser = serial.Serial('/dev/ttyUSB0',9600)
rec=cv2.createLBPHFaceRecognizer();
rec.load("trainer/trainer.yml")
id=0
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,3,1,0,1)
thresholdValue = 150

firstFrame = None

Id=raw_input('enter your id')
sampleNum=0

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
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
		if cv2.contourArea(c) < 5000:
			continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		sampleNum=sampleNum+1
		cv2.imwrite("data_set/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
		cv2.imshow('frame1',frame)
		cv2.imshow('frame',frame)	
		

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif sampleNum >20:
		break    

    cv2.putText(frame, "In: {}".format(str(textIn)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Out: {}".format(str(textOut)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)



# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


	
