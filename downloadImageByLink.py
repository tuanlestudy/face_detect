import urllib
import cv2
import numpy as np
import os
import shutil

def store_raw_images():
    #neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00007846'
    #plant, flora, plat life
    s1 = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00017222"
    #geological formation, formation
    s2 = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09287968"
    #natural object
    
    #sport, athletics
    s3 = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513"
    #artifact, athletics
    s4 = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00021939"
    #fungus
    s5 = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n12992868"
    #person, individual, someone, somebody, mortal, soul
    s6 = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00007846"
    #animal, animate being, beast, brute, creature, fauna
    s7 = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00015388"

    folder="neg"
    neg_images_link = s3
    neg_image_urls = urllib.urlopen(neg_images_link).read().decode()

    if not os.path.exists(folder):
        os.makedirs(folder)

    pic_num = 1

    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.urlretrieve(i, folder+"/"+str(pic_num)+'.jpg')
            img = cv2.imread(folder+"/"+str(pic_num)+'.jpg',cv2.IMREAD_GRAYSCALE)
            resized_image = cv2.resize(img,(100,100))
            cv2.imwrite(folder+"/"+str(pic_num)+'.jpg', resized_image)
            pic_num += 1
        except Exception as e:
            print(str(e))



def find_uglies():
    if not os.path.exists('uglies'):
        os.makedirs('uglies')
    match = False
    pic_num = 1
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        #print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

store_raw_images()
find_uglies()

print('Done !!!')
