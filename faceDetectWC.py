#!/usr/bin/env python
""" Starting script for the face recognition system.
"""

import sys
import os
import numpy as np
from face_recognition_system.videocamera import VideoCamera
from face_recognition_system.detectors import FaceDetector
import face_recognition_system.operations as op
import cv2
from cv2 import __version__
import datetime
from PIL import ImageGrab
import time
from IPython.display import Image
import shutil

def get_images(frame, faces_coord, shape):
    """ Perfrom transformation on original and face images.

    This function draws the countour around the found face given by faces_coord
    and also cuts the face from the original image. Returns both images.

    :param frame: original image
    :param faces_coord: coordenates of a rectangle around a found face
    :param shape: indication of which shape should be drwan around the face
    :type frame: numpy array
    :type faces_coord: list of touples containing each face information
    :type shape: String
    :return: two images containing the original plus the drawn contour and
             anoter one with only the face.
    :rtype: a tuple of numpy arrays.
    """
    if shape == "rectangle":
        faces_img = op.cut_face_rectangle(frame, faces_coord)
        frame = op.draw_face_rectangle(frame, faces_coord)
    elif shape == "ellipse":
        faces_img = op.cut_face_ellipse(frame, faces_coord)
        frame = op.draw_face_ellipse(frame, faces_coord)
    faces_img = op.normalize_intensity(faces_img)
    faces_img = op.resize(faces_img)
    return (frame, faces_img)

def func_addperson(people_folder, shape, folder):
    count = 0
    while (count < 5):
        raw_input("I will now take 20 pictures. Press ENTER when ready.")
        video = VideoCamera()
        detector = FaceDetector('face_recognition_system/frontal_face.xml')
        counter = 1
        timer = 0
        cv2.namedWindow('Video Feed', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('Saved Face', cv2.WINDOW_NORMAL)
        while counter < 21:
            frame = video.get_frame()
            face_coord = detector.detect(frame)
            if len(face_coord):
                frame, face_img = get_images(frame, face_coord, shape)
                # save a face every second, we start from an offset '5' because
                # the first frame of the camera gets very high intensity
                # readings.
                if timer % 100 == 5:
                    now = datetime.datetime.now()
                    stringnow = str("%d" % now.year + "%d" % now.month + "%d" % now.day + "%d" % now.hour + "%d" % now.minute + "%d" % now.second)
                    cv2.imwrite(folder + '/' + str(stringnow) + '.jpg', face_img[0])                            
                    print ("Images Saved: " + str(stringnow))
                    cv2.imshow('Saved Face', face_img[0])
                    counter+=1
            cv2.putText(frame, str(timer % 100), (5, frame.shape[0] - 5),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (206, 0, 209), 2, cv2.LINE_AA)
            cv2.imshow('Video Feed', frame)
            cv2.waitKey(50)
            timer += 5   
        count += 1

def add_person(people_folder, shape):
    """ Funtion to add pictures of a person

    :param people_folder: relative path to save the person's pictures in
    :param shape: Shape to cut the faces on the captured images:
                  "rectangle" or "ellipse"
    :type people_folder: String
    :type shape: String
    """
    person_name = raw_input('What is the name of the new person: ').lower()
    folder = people_folder + person_name
    if not os.path.exists(folder):
        os.mkdir(folder)
        func_addperson(people_folder, shape, folder)
    else:
        addmore = raw_input("This name already exists. Do you want add more data? (yes/no)")
        if (addmore == "no"):
            sys.exit()
        elif(addmore == "yes"):
            func_addperson(people_folder, shape, folder)

def add_person_pics(people_folder, shape):
    person_name = raw_input('What is the name of the new person: ').lower()
    folder = people_folder + person_name
    if not os.path.exists(folder):
        os.mkdir(folder)
        func_addpersonpics(folder, shape)
    else:
        addmore = raw_input("This name already exists. Do you want add more data? (yes/no)")
        if (addmore == "no"):
            sys.exit()
        elif(addmore == "yes"):
            func_addpersonpics(folder, shape)

def mkdir(text):
    if not os.path.exists(text):
        os.makedirs(text)
        
def func_addpersonpics(folder, shape):
    count = 0 
    mkdir('data/pics')
    mkdir('data/pos')
    try:
        file_images = raw_input("Enter the images' direction: ")
    except:
        print("NO FOUND FOLDER !!!")
        sys.exit()
    cascade_faces = [
    "haarcascade_frontalface_default.xml",
    "haarcascade_frontalface_alt.xml",
    "haarcascade_frontalface_alt2.xml",
    "haarcascade_frontalface_alt_tree.xml",
    "haarcascade_profileface.xml"]

    #copy file to pics folder
    print("Copying images .....")
    for file_type in [file_images]:
        for img in os.listdir(file_type):
            imagePath = file_type+'/'+img
            newimagePath = "data/pics/"+img
            shutil.copy2(imagePath,newimagePath)
    print("Complete to copy images")
    processpercent = 0
    print("Faces detecing ..... " + str(processpercent) + "%")

    for i in cascade_faces:
        cascadePath = "haarcascade/"+i 
        #print (cascadePath)
        detector = FaceDetector(cascadePath)
        for file_type in ['data/pics']:
            for img in os.listdir(file_type):
                imagePath = file_type+'/'+img
                frame = cv2.imread(imagePath)
                face_coord = detector.detect(frame)
                if len(face_coord):
                    frame, face_img = get_images(frame, face_coord, shape)
                    now = datetime.datetime.now()
                    #cv2.imwrite(folder + '/' + img, face_img[0])  

                    #after create new function detect faces, will delete this line                          
                    cv2.imwrite('data/crop/'+ img, face_img[0])                            
                        
                    print ("Images Saved: " + img)
                    cv2.imshow("frame after", cv2.resize(frame, (240, 320)))
                    cv2.waitKey(100)
                    count += 1
                    #copy to pos
                    newimagePath = "data/pos/"+img
                    shutil.move(imagePath, newimagePath)
        processpercent += 20
        print("Faces detecing ..... " + str(processpercent) + "%")
    
    #os.rmdir()
    #shutil.rmtree()

    while True:
        ans = raw_input("Do you want add more? (y/n)")
        if (ans == "y"):
            func_addpersonpics(folder, shape)
        else:
            sys.exit()



def recognize_people(people_folder, shape):
    """ Start recognizing people in a live stream with your webcam

    :param people_folder: relative path to save the person's pictures in
    :param shape: Shape to cut the faces on the captured images:
                  "rectangle" or "ellipse"
    :type people_folder: String
    :type shape: String
    """
    try:
        people = [person for person in os.listdir(people_folder)]
    except:
        print "Have you added at least one person to the system?"
        sys.exit()
    print "This are the people in the Recognition System:"
    for person in people:
        print "-" + person

    print 30 * '-'
    print "   POSSIBLE RECOGNIZERS TO USE"
    print 30 * '-'
    print "1. EigenFaces"
    print "2. FisherFaces"
    print "3. LBPHFaces"
    print 30 * '-'

    choice = check_choice()

    detector = FaceDetector('face_recognition_system/frontal_face.xml')
    if choice == 1:
        recognizer = cv2.face.EigenFaceRecognizer_create()
        threshold = 4000
    elif choice == 2:
        recognizer = cv2.face.FisherFaceRecognizer_create()
        threshold = 300
    elif choice == 3:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        threshold = 105
    images = []
    labels = []
    labels_people = {}
    for i, person in enumerate(people):
        labels_people[i] = person
        for image in os.listdir(people_folder + person):
            images.append(cv2.imread(people_folder + person + '/' + image, 0))
            labels.append(i)
    try:
        recognizer.train(images, np.array(labels))
    except:
        print "\nOpenCV Error: Do you have at least two people in the database?\n"
        sys.exit()

    video = VideoCamera()
    while True:
        frame = video.get_frame()
        faces_coord = detector.detect(frame, False)
        if len(faces_coord):
            frame, faces_img = get_images(frame, faces_coord, shape)
            for i, face_img in enumerate(faces_img):
                if __version__ == "3.1.0":
                    collector = cv2.face.MinDistancePredictCollector()
                    recognizer.predict(face_img, collector)
                    conf = collector.getDist()
                    pred = collector.getLabel()
                else:
                    pred, conf = recognizer.predict(face_img)
                print "Prediction: " + str(pred)
                print 'Confidence: ' + str(round(conf))
                print 'Threshold: ' + str(threshold)
                if conf < threshold:
                    cv2.putText(frame, labels_people[pred].capitalize(),
                                (faces_coord[i][0], faces_coord[i][1] - 2),
                                cv2.FONT_HERSHEY_PLAIN, 1.7, (206, 0, 209), 2,
                                cv2.LINE_AA)
                else:
                    cv2.putText(frame, "Unknown",
                                (faces_coord[i][0], faces_coord[i][1]),
                                cv2.FONT_HERSHEY_PLAIN, 1.7, (206, 0, 209), 2,
                                cv2.LINE_AA)

        cv2.putText(frame, "ESC to exit", (5, frame.shape[0] - 5),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (206, 0, 209), 2, cv2.LINE_AA)
        cv2.imshow('Video', frame)
        if cv2.waitKey(100) & 0xFF == 27:
            sys.exit()

def check_choice():
    """ Check if choice is good
    """
    is_valid = 0
    while not is_valid:
        try:
            choice = int(raw_input('Enter your choice [1-3] : '))
            if choice in [1, 2, 3]:
                is_valid = 1
            else:
                print "'%d' is not an option.\n" % choice
        except ValueError, error:
            print "%s is not an option.\n" % str(error).split(": ")[1]
    return choice

if __name__ == '__main__':
    print 30 * '-'
    print "   POSSIBLE ACTIONS"
    print 30 * '-'
    print "1. Add person to the recognizer system from webcam"
    print "2. Start recognizer from webcam"
    print "3. Add person to the recognizer from pictures"
    print "0. Exit"
    print 30 * '-'

    CHOICE = check_choice()

    PEOPLE_FOLDER = "face_recognition_system/people/"
    SHAPE = "ellipse"
    if CHOICE == 1:
        if not os.path.exists(PEOPLE_FOLDER):
            os.makedirs(PEOPLE_FOLDER)
        add_person(PEOPLE_FOLDER, SHAPE)
    elif CHOICE == 2:
        recognize_people(PEOPLE_FOLDER, SHAPE)
    elif CHOICE == 3:
        if not os.path.exists(PEOPLE_FOLDER):
            os.makedirs(PEOPLE_FOLDER)
        add_person_pics(PEOPLE_FOLDER, SHAPE)
    elif CHOICE == 0:
        sys.exit()
