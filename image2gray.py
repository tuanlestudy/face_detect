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
    try:
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
    except Exception as e:
        print(str(e))

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

def find_uglies(textPath):
    i=len(textPath)-1
    while i > 0:
    	if(textPath[i]=='/'):
    		dirPath=textPath[:i+1]
    		break
        i=i-1
    match = False
    if not os.path.exists(dirPath+'uglies'):
        os.makedirs(dirPath+'uglies')
    for file_type in [dirPath+'neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir(dirPath+'uglies'):
                try:
                    current_image_path = dirPath+str(file_type)+'/'+str(img)
                    #print(current_image_path)
                    ugly = cv2.imread(dirPath+'uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        #os.remove(current_image_path)
                except Exception as e:
                    print(str(e))


def create_pos_n_neg(textPath):
    i=len(textPath)-1
    while i > 0:
    	if(textPath[i]=='/'):
    		dirPath=textPath[:i+1]
    		break
        i=i-1

    for file_type in [dirPath+'neg']:
        
        for img in os.listdir(file_type):

            if file_type == (dirPath+'pos'):
                line = dirPath+file_type+'/'+img+' 1 0 0 50 50\n'
                with open(dirPath+'info.dat','a') as f:
                    f.write(line)
            elif file_type == (dirPath+'neg'):
                line = dirPath+file_type+'/'+img+'\n'
                with open(dirPath+'bg.txt','a') as f:
                    f.write(line)


if __name__ == "__main__":
    # Get user supplied values
    # #textPath = sys.argv[1]
    textPath="data_pics/people/tokimngoc/raw/listpics.txt"
    #readFile(textPath)
    find_uglies(textPath)


