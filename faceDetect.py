import cv2
import sys
import numpy as np
import time
import shutil
#------------------------------------------------

def readFile(textPath):
    temp=""
    count = 0
    #print (textPath)
    i=len(textPath)-1
    while i > 0:
    	if(textPath[i]=='/'):
    		dirPath=textPath[:i+1]
    		break
        i=i-1
    #print (dirPath)
    f = file(textPath, "r")
    line = f.readline()
    while(len(line)):
        line = f.readline()
        temp=""+str(line)
        temp2 = temp[:(len(temp)-1)]
        imagePath = dirPath+temp2
        print imagePath
        checkFaceImage(imagePath,dirPath,temp2)
        count = count + 1
        time.sleep(1)
        print (count)




def checkFaceImage(imagePath,dirPath,nameimage):

    # Create the haar cascade
    face_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
    #eye_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_eye.xml")

    # Read the image
    img = cv2.imread(imagePath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    print("Found {0} faces!".format(len(faces)))
    #print(imagePath)
    #print('\n')

    #crop image
    if(len(faces) > 0) :
        crop_img = img[y:y+h, x:x+w]
        newcropimage = dirPath+"crop/"+nameimage
        cv2.imwrite(newcropimage,crop_img)
        newimage = dirPath+"true/"+nameimage
        #cv2.imwrite(newimage,img)
        shutil.copy2(imagePath,newimage)
    else:
        newimage = dirPath+"false/"+nameimage
        #cv2.imwrite(newimage,img)
                


if __name__ == "__main__":
	# Get user supplied values
	#textPath = sys.argv[1]
	textPath="data_pics/people/tokimngoc/raw/listpics.txt"
	readFile(textPath)










































