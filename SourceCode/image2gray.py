import cv2
import sys
import numpy as np
import time
import shutil
import os
#------------------------------------------------

def facedetect():
    mkdir('gray')
    mkdir('crop')
    for file_type in ['pics']:
        for img in os.listdir(file_type):
            imagePath = file_type+'/'+img
            imgread = cv2.imread(imagePath)
            resized_image = cv2.resize(imgread,(100,100))
            gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            newgrayimage = "gray/"+img
            cv2.imwrite(newgrayimage,gray)
            newcropimage = "crop/"+img
            shutil.move(newgrayimage, newcropimage)
            cv2.imshow("Pictures", cv2.resize(imgread, (200, 200)))
            cv2.waitKey(100)

def mkdir(text):
    if not os.path.exists(text):
        os.makedirs(text)

if __name__ == "__main__":
    facedetect()









































