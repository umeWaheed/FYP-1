import cv2
import os
# import sys
import time
from threading import Timer
import re # regular expresions
import Global
# import numpy
# import dlib
#import pygame


class Train:
    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []
    # list to hold names for all subjects
    names = [""]


#facePath = "C:\\Users\\ACER\\Downloads\\opencv\\sources\\data\\lbpcascades\\lbpcascade_frontalface.xml"
facePath = "lbpcascade_frontalface.xml"
#eyePath = "C:\\Users\\ACER\\Downloads\\opencv\\sources\\data\\haarcascades\\haarcascade_eye.xml"
#eyeCascade = cv2.CascadeClassifier(eyePath)
#video_capture = cv2.VideoCapture(0)
# os.mkdir('train')
index = 0

def detect_face(image):
    faceCascade = cv2.CascadeClassifier(facePath)

    # Read the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces)==0:
        print('none')
        return None,None
    else:
        print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    (w,x,y,h) = faces[0]
    draw_rectangle(image,(x,w,y,h))
    cv2.imshow('user',image)
    cv2.waitKey(100)
    return gray[y:y+h,x:x+w],faces[0]


def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)

    for dir_name in dirs:
        prepare_user(dir_name)
        '''if not dir_name.startswith("s"):
            continue
        if not pattern.match(dir_name):
            continue
        label = int(dir_name[len(dir_name)-1])  # get the last character as label of the users
        names.insert(label,dir_name[:-2])  # insert subject name at its label position

    # build path of directory containing images for current subject subject
    # sample subject_dir_path = "training-data/s1"
        subject_dir_path = data_folder_path + "/" + dir_name

    # get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:
            # ignore system files like .DS_Store
            if image_name.startswith("."):
                continue
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)

            #cv2.imshow("Training on image...", image)
            #cv2.waitKey(100)
            # detect face
            #face,rect = detect_face(image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            #if face is not None:
            faces.append(gray)
            labels.append(label)'''

    for n in Train.names:
        if n == "":
            Train.names.remove(n)
    return Train.faces, Train.labels, Train.names


def prepare_user(dir_name):
    # global faces, labels, names
    pattern = re.compile('^[a-zA-Z]*[_]{1}[1-9]{1}$')  # if name is like abc_1

    if pattern.match(dir_name):
        label = int(dir_name[len(dir_name)-1])  # get the last character as label of the users
        Train.names.insert(label,dir_name[:-2])  # insert subject name at its label position

    # build path of directory containing images for current subject subject
    # sample subject_dir_path = "training-data/s1"
        subject_dir_path = 'training_data' + "/" + dir_name

    # get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:
            # ignore system files like .DS_Store
            if image_name.startswith("."):
                continue
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)

            #cv2.imshow("Training on image...", image)
            #cv2.waitKey(100)
            # detect face
            #face,rect = detect_face(image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            Train.faces.append(gray)
            Train.labels.append(label)
        return Train.faces, Train.labels,Train.names


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)


def draw_text(img,text):
    cv2.putText(img, text, (10, 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


def predict(test_img,face_recognizer):
    # make a copy of the image as we don't want to change original image
    #img = test_img.copy()
    # detect face from the image
    # predict the image using our face recognizer
    label,confidence = face_recognizer.predict(test_img)
    print("label=", label, "conf=", confidence)
    if confidence > 35:
        Global.close_to = label         # store the person user resembles
        label = 0
    return label
    # get name of respective label returned by face recognizer
    '''label_text = subjects[label]

    # draw a rectangle around face detected
    draw_rectangle(img, rect)
    # draw name of predicted person
    draw_text(img, label_text, rect[0], rect[1] - 5)
    print(label, " ", confidence)
    
        pygame.mixer.init()
        sound = pygame.mixer.music.Sound("siren.wav")
        sound.play()'''


def capture_img(vid):
    global index
    #vid = cv2.VideoCapture(0)
    time.sleep(0.1) # for brighter picture
    s,im = vid.read()
    # im = vid.read()
    im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    #vid.release()
    return im
    # cv2.imshow('Test Picture',im)
    #index += 1
    #img_name = 'img'+ str(index)+'.jpg'
    #cv2.imwrite(os.path.join('training_data\\s0',img_name), im)
    # cv2.waitKey(0)


def start_video():
    global video_capture, index
    """t = Timer(10, capture_img)
    t.start()"""
    while True:
        """if not t.is_alive() and index < 5:
            t = Timer(10, capture_img)
            t.start()"""

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        # frame = cv2.flip(frame,1,0)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        """faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )"""
        face, rect = detect_face(frame)
        (x,w,y,h) = rect

        '''if face is not None:
            eyes = eyeCascade.detectMultiScale(gray[y:y+h,x:x+w])
            eye_space = frame[y:y+h,x:x+w]
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(eye_space, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            label = predict(gray)
            print(label)
            label_text = subjects[label]

            # draw a rectangle around face detected
            draw_rectangle(frame, rect)
            # draw name of predicted person
            draw_text(frame, label_text, rect[0], rect[1] - 5)
            # Display the resulting frame
'''
        cv2.imshow('Video',frame)
        # Draw a rectangle around the faces
        """for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)"""

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def prepare_data():
    t = Timer(10,capture_img())
    t.start()
    if not t.is_alive() and index<5:
        t.start()


#start_video()
# prepare_training_data()
'''subjects = ['user1', 'emma','user3']
print('preparing data...')
faces, labels = prepare_training_data("training_data")
print('data prepared')
print('total faces:', len(faces))
print('total labels:', labels)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, numpy.array(labels))
# When everything is done, release the capture
start_video()
video_capture.release()
cv2.destroyAllWindows()'''

# t = Timer(10,capture_img)
# t.start()
