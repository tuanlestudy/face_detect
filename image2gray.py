import cv2
import numpy as nu
import os
import sys
import shutil

def readFile(textPath):
    temp=""
    count = 0
    i=len(textPath)-1
    while i > 0:
    	if(textPath[i]=='/'):
    		dirPath=textPath[:i+1]
    		break
        i=i-1
    f = file(textPath, "r")
    line = f.readline()
    while(len(line)):
        line = f.readline()
        temp=""+str(line)
        temp2 = temp[:(len(temp)-1)]
        imagePath = dirPath+temp2
        print (imagePath)
        image2gray(imagePath,dirPath,temp2)
        count = count + 1
        print (count)

def image2gray(imagePath,dirPath,nameimage):
    if not os.path.exists(dirPath+'neg'):
        os.makedirs(dirPath+'neg')
    try:
        img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        resized_image = cv2.resize(img,(100,100))
        newgrayimage = dirPath+'neg/'+nameimage
        cv2.imwrite(newgrayimage, resized_image)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
	# Get user supplied values
	textPath = sys.argv[1]
	#textPath="data_pics/people/tokimngoc/raw/listpics.txt"
	readFile(textPath)