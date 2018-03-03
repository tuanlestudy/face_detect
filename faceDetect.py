import cv2
import sys
import numpy as np
import time
import shutil
import os
#------------------------------------------------

def facedetect():
    countfaces = 0

    cascade_faces = [
    "haarcascade_frontalface_default.xml",
    "haarcascade_frontalface_alt.xml",
    "haarcascade_frontalface_alt2.xml",
    "haarcascade_frontalface_alt_tree.xml",
    "haarcascade_profileface.xml"]
    for i in cascade_faces:
        print(i)
        for file_type in ['pics']:
            for img in os.listdir(file_type):
                imagePath = file_type+'/'+img
                cascadePath = "haarcascade/"+i  
                countfaces += checkFaceImage(imagePath, img, cascadePath, 0)

    cascade_eyes = [
    "haarcascade_eye_tree_eyeglasses.xml",
    "haarcascade_eye.xml",
    "haarcascade_righteye_2splits.xml"]
    for i in cascade_eyes:
        print(i)
        for file_type in ['pics']:
            for img in os.listdir(file_type):
                imagePath = file_type+'/'+img
                cascadePath = "haarcascade/"+i  
                countfaces += checkFaceImage(imagePath, img, cascadePath, 1)

    
    #print ('Total Pictures: ' + str(count))
    print ('Found:          ' + str(countfaces) + ' faces')


def checkFaceImage(imagePath,nameimage, cascadePath, check):
    countface = 0
    face_cascade = cv2.CascadeClassifier(cascadePath)

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
        if(check == 0):
            crop_img = img[y:y+h, x:x+w]
            newcropimage = "crop/"+nameimage
            grayface = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(newcropimage,grayface)

        newimagePath = "pos/"+nameimage
        imageShow = cv2.imread(imagePath)
        cv2.imshow("Pictures", cv2.resize(imageShow, (240, 320)))
        cv2.waitKey(100)
        #cv2.imwrite(newimage,img)
        #shutil.copy2(imagePath,newimage)
        #os.rename("path/to/current/file.foo", "path/to/new/desination/for/file.foo")
        shutil.move(imagePath, newimagePath)
        countface +=len(faces)
    else:
        newimage = "neg/"+nameimage
        #cv2.imwrite(newimage,img)
        #shutil.copy2(imagePath,newimage)
    return countface

def mkdir(text):
    if not os.path.exists(text):
        os.makedirs(text)

if __name__ == "__main__":
    facedetect()









































