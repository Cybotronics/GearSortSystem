import cv2
cam = cv2.VideoCapture(0)
print 'Default Resolution is ' + str(int(cam.get(3))) + 'x' + str(int(cam.get(4)))
w=1024
h=768
cam.set(3,w)
cam.set(4,h)
print 'Now resolution is set to ' + str(w) + 'x' + str(h)



detector=cv2.CascadeClassifier('gear.xml')

Id=raw_input('enter your id')
sampleNum=0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				sampleNum=sampleNum+1

				cv2.imwrite("data_set/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
				cv2.imshow('frame1',img) 
    cv2.imshow('frame',img)  
    #wait for 100 miliseconds 
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum>20:
        break
cam.release()
cv2.destroyAllWindows()
