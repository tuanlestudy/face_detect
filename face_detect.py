import cv2
import sys
import numpy as np 

# Get user supplied values
#imagePath = sys.argv[1]
imagePath = 'ngoc0001.jpg'

# Create the haar cascade
face_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_eye.xml")

# Read the image
img = cv2.imread(imagePath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
#faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, #minSize=(30, 30), #flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
	
	# Draw a rectangle around the eyes
	#roi_gray = gray[y:y+h, x:x+w]
	#roi_color = img[y:y+h, x:x+w]
	#eyes = eye_cascade.detectMultiScale(roi_gray)
	#for (ex, ey, ew, eh) in eyes:
	#	cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)
	

print("Found {0} faces!".format(len(faces)))

if(len(faces)>0):
	crop_img = img[y:y+h, x:x+w]
	cv2.imwrite('test01.jpg',crop_img)	#save crop image
	cv2.imshow("Faces found", crop_img)
	cv2.waitKey(0)

#cv2.imshow("Faces found", img)
#cv2.waitKey(0)
