import cv2
import sys
import numpy as np
import time
import shutil
import os
#------------------------------------------------

def faceDetect(textPath, dirPath, imgPath):
    temp=""
    count = 0
    countface = 0
    num_lines = sum(1 for line in open(textPath))
    try:
        f = file(textPath, "r")
        #line = f.readline()
        for x in range(0,num_lines):
            line = f.readline()
            temp=""+str(line)
            temp2 = temp[:(len(temp)-1)]
            imagePath = imgPath+temp2
            print (imagePath)
            countface += checkFaceImage(imagePath,dirPath,temp2)
            count += 1
            x += 1
        f.close()
    except Exception as e:
        print(str(e))
    print ("Total: " + str(count) + " pictures")
    print ("Found: " + str(countface) + " faces")




def checkFaceImage(imagePath,dirPath,nameimage):

    countface = 0

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

    #print("Found {0} faces!".format(len(faces)))

    #crop image
    if(len(faces) > 0) :
        crop_img = img[y:y+h, x:x+w]
        newcropimage = dirPath+"crop/"+nameimage
        cv2.imwrite(newcropimage,crop_img)
        newimage = dirPath+"pos/"+nameimage
        #cv2.imwrite(newimage,img)
        shutil.copy2(imagePath,newimage)
        countface +=len(faces)
    else:
        newimage = dirPath+"neg/"+nameimage
        #cv2.imwrite(newimage,img)
        shutil.copy2(imagePath,newimage)
    return countface

def mkdir(dirPath, text):
    if not os.path.exists(dirPath+text):
        os.makedirs(dirPath+text)

if __name__ == "__main__":
	# Get user supplied values
    #textPath = sys.argv[1]
    textPath="data_pics/people/tokimngoc/raw/list.txt"
    
    i=len(textPath)-1
    while i > 0:
    	if(textPath[i]=='/'):
    		dirPath=textPath[:i-3]
    		break
        i=i-1
    
    i=len(textPath)-1
    while i > 0:
    	if(textPath[i]=='/'):
    		imgPath=textPath[:i+1]
    		break
        i=i-1

    mkdir(dirPath, 'crop')
    mkdir(dirPath, 'neg')
    mkdir(dirPath, 'pos')

    faceDetect(textPath, dirPath, imgPath)









































