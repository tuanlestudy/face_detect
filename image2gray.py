import cv2
import numpy as np
import os
import sys
import shutil

def faceDetect(textPath, imgPath):
    temp=""
    count = 0
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
            image2gray(imagePath,temp2)
            count += 1
            x += 1
        f.close()
    except Exception as e:
        print(str(e))
    print (count)

def image2gray(imagePath,nameimage):
    if not os.path.exists('neg'):
        os.makedirs('neg')
    try:
        img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        resized_image = cv2.resize(img,(100,100))
        newgrayimage = 'neg/'+nameimage
        cv2.imwrite(newgrayimage, resized_image)
    except Exception as e:
        print(str(e))



def create_pos_n_neg():
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            if file_type == ('pos'):
                line = file_type+'/'+img+' 1 0 0 50 50\n'
                with open('info.dat','a') as f:
                    f.write(line)
            elif file_type == ('neg'):
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)

if __name__ == "__main__":
    # Get user supplied values
    #textPath = sys.argv[1]
    textPath="pics/list.txt"
    imgPath=""
    i=len(textPath)-1
    while i > 0:
        if(textPath[i]=='/'):
            imgPath=textPath[:i+1]
            break
        i=i-1

    #faceDetect(textPath, imgPath)
    #find_uglies(textPath)
    create_pos_n_neg()




def find_uglies(textPath, dirPath):
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

