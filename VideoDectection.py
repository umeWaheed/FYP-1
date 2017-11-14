import cv2
import os
import sys
from threading import Timer

cascPath = "C:\\Users\\ACER\\Downloads\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
# os.mkdir('train')
index = 0


def capture_img():
    global index
    video_capture = cv2.VideoCapture(0)
    s,im = video_capture.read()
    cv2.imshow('Test Picture',im)
    index += 1
    img_name = 'img'+ str(index)+'.jpg'
    cv2.imwrite(os.path.join('train',img_name), im)
    cv2.waitKey(0)
    video_capture.release()
    cv2.destroyAllWindows()


def start_video():
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()


t = Timer(10,capture_img)
t.start()