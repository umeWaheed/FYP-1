import cv2
import os
import time
import MainFace1
import Global

# Get user supplied values
imagePath = "test.png"
cascPath = facePath = "lbpcascade_frontalface.xml"
# cascPath = facePath = "C:\\Users\\ACER\\Downloads\\opencv\\sources\\data\\lbpcascades\\lbpcascade_frontalface.xml"
index = 0
# Create the haar cascade
'''faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.2,
    minNeighbors=2,
    minSize=(20, 20),
    flags=cv2.CASCADE_SCALE_IMAGE
)'''


def facecrop(img, flag=False):
    cascade = cv2.CascadeClassifier(cascPath)

    # img = cv2.imread(img)

    '''minisize = (img.shape[1],img.shape[0])
    miniframe = cv2.resize(img, minisize)

    faces = cascade.detectMultiScale(miniframe)'''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=2,
        minSize=(20, 20),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces) != 0:
        f = faces[0]
        # for f in faces:
        x, y, w, h = [v for v in f]
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255))
        # cv2.imshow('before',img)
        # cv2.waitKey(0)

        sub_face = img[y:y+h, x:x+w]
        # fname, ext = os.path.splitext(image)
        if flag:        # if image is to be saved
            img_name = 'img' + str(index) + '.jpg'
            cv2.imwrite(os.path.join(path+'\\'+img_name), sub_face)
            # cv2.imwrite(fname+"_cropped_"+ext, sub_face)
            # cv2.imshow('cropped',sub_face)
            # cv2.waitKey(0)
        return sub_face


'''dir = os.listdir('training_data/s'+str(lbl))
for img in dir:
    facecrop('training_data/s0/'+img)
print("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    print("face : ",x,y,w,h)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.imshow("Faces found", image)
cv2.waitKey(0)'''


def capture_img():
    global index
    time.sleep(0.1)     # for brighter picture
    s, im = Global.vid.read()
    if s:
        # im = Global.vid.read()
        im = cv2.flip(im, 1)
    # im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Test Picture',im)
    # img_name = 'img'+ str(index)+'.jpg'
    # cv2.imwrite(os.path.join(path+'\\'+img_name), im)
    # cv2.waitKey(0)
        return im
    else:
        print ('no image')


def gather_samples(name, lbl):
    global path, index
    flag = True
    # lbl = str(len(MainFace1.FaceVal().subjects)) #the next label number
    # MainFace1.FaceVal().subjects.append('new')
    path = 'training_data\\'+name+'_'+str(lbl)
    if not os.path.exists(path):
        os.makedirs(path)
    # vid = cv2.VideoCapture(0)
    while index < 10:
        img = capture_img()
        image = facecrop(img, True)
        # time.sleep(5)
        index += 1

    MainFace1.load_new(name, lbl)    # load the new user into the model


'''s_path = 'training_data\\b'
index1=0
for image in os.listdir(s_path):
    # rect, face = detect_face(image)
    index1 +=1
    facecrop(s_path+'\\'+image,True)'''