import FacialLandmark
import Face, Analyse
import VideoDetection
import numpy
# import argparse
import dlib
import cv2
import time
from VideoDetection import Train
import FaceDetection
import threading
import Global
from Global import Points
import Frames
# from User import UserInfo


face_recognizer = cv2.face.LBPHFaceRecognizer_create()
#current_user = UserInfo()


class FaceVal:
    '''contains data regarding the label'''
    label = 0
    video = None
    subjects = ['unknown']

    def __init__(self):
        FaceVal.video = Global.vid
        '''file = open('user_info/subjects.txt')
        for line in file:
            self.subjects.append(line.rstrip('\n'))  # add subjects into the array label wise'''

    def load_settings(self):
        global faces, labels, names
        print('preparing data...')
        '''face_recognizer.read('recognizers/trainner.yml')
        time.sleep(10)'''
        faces, labels, names = VideoDetection.prepare_training_data("training_data")
        for name in names:
            FaceVal.subjects.append(name)
        print(FaceVal.subjects)
        print('data prepared')
        print('total faces:', len(Train.faces))
        print('total labels:', Train.labels)

        face_recognizer.train(Train.faces, numpy.array(Train.labels))
        #face_recognizer.write('recognizers/trainner.yml')
        # crop the image of the user from video stream
        img = FaceDetection.facecrop(FaceDetection.capture_img())
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            FaceVal.label = VideoDetection.predict(gray, face_recognizer)
            print(FaceVal.label)
        else:
            print ('error reading image')
        #current_user.set_user(self.subjects[FaceVal.label],FaceVal.label)
        #print(current_user.name+" "+str(current_user.label))


def monitor():
    Analyse.load_settings()
    video_capture = Global.vid
    idle_duration = 0
    idle_time = 0
    usage_time = 0
    usage_duration = 0
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # (args["shape_predictor"])
    # eyes blink count
    eye_thereshold = 0.22
    eye_frames = 3
    counter = 0
    total = 0
    (lStart, lEnd) = FacialLandmark.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = FacialLandmark.FACIAL_LANDMARKS_IDXS["right_eye"]

    time.sleep(0.2)

    # t4 = threading.Thread(target=Analyse.check_movement, args=(Points.x, Points.y, Points.w, Points.h))

    while not Global.shutdown:     # video_capture.isOpened():
        # t4.start()
        ret, frame = video_capture.read()#(args['image'])

        # frame = video_capture.read()

        if not ret:
            break

        frame = Face.resize(frame, width=400)
        frame = cv2.flip(frame,1)
        #cv2.add(frame, numpy.array([100.0]))       increase brightness
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #label = VideoDetection.predict(gray,face_recognizer)    ##
        #print(label)
        label_text = FaceVal.subjects[FaceVal.label]
        #VideoDetection.draw_text(frame, label_text)

        # detect faces in the grayscale image
        rects = detector(gray, 0)

        if len(rects) == 0:     # if user is not available stop processing
            if not Global.is_available:     # if already false
                idle_duration = time.time()-idle_time
            else:               # set start of idle time and set available to false
                usage_duration = time.time()-usage_time     # the time user was sitting
                print('used for ', usage_duration)
                Analyse.write_usage(time.strftime("%X"), 'usage duration ',usage_duration)
                Global.is_available = False
                idle_time = time.time()      # start of idle time
                print('idle started ',time.asctime(time.localtime(time.time())))
                Analyse.write_usage(time.strftime("%X"), 'idle started ', 0)
                if Global.usage_exceed:
                    Global.usage_exceed = False            # if the usage was exceeded note the time and write in file

        else:
            if not Global.is_available:     # if user is now available
                print('idle for = ', idle_duration)
                Analyse.write_usage(time.strftime("%X"), 'idle duration ', idle_duration)
                usage_time = time.time()    # set the time user started usage
                print('usage started ', time.asctime(time.localtime(time.time())))
                Analyse.write_usage(time.strftime("%X"), 'usage started ', 0)
                Global.is_available = True
            else:
                usage_duration = time.time()-usage_time
                if usage_duration > Points.usage and not Global.usage_exceed:
                    Global.usage_exceed = True
                    Analyse.write_usage('usage exceed '+str(time.asctime(time.localtime(time.time()))))
                    print('use less')

                # for rect in rects:
                rect = rects[0]
                if rect is not None:
                    # determine the facial landmarks for the face region, then
                    # convert the facial landmark (x, y)-coordinates to a NumPy
                    # array
                    shape = predictor(gray, rect)

                    shape = FacialLandmark.shape_to_np(shape)
                    leftEye = shape[lStart:lEnd]
                    rightEye = shape[rStart:rEnd]
                    leftEAR = Face.eye_aspect_ratio(leftEye)
                    rightEAR = Face.eye_aspect_ratio(rightEye)

                    (x, y, w, h) = FacialLandmark.rect_to_bb(rect)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # Points.x, Points.y, Points.w, Points.h = x, y, w, h

                    # show the face number
                    cv2.putText(frame, label_text, (x - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # average the eye aspect ratio together for both eyes
                    ear = (leftEAR + rightEAR) / 2.0

                    if ear < eye_thereshold:
                        counter += 1
                    else:
                        if counter >= eye_frames:
                            total += 1
                        counter = 0

                    if total == 0:
                        old_time = time.time()

                    if time.time() - old_time > 59:
                        # after a minute has passed write the blinks of user and check his movement
                        #Analyse.write_blinks(time.asctime(time.localtime(time.time())), total)
                        Analyse.write_blinks(time.strftime("%X"), total)
                        Analyse.check_movement(x, y, w, h)

                        if total < 17:
                            Global.engine.say("Blink more")
                            Global.engine.setProperty('rate', 120)
                            Global.engine.runAndWait()
                            cv2.putText(frame, "blink more!!", (300, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        total=0


                    cv2.putText(frame, "Blinks: {}".format(total), (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        #cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                                  #  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                        # convert dlib's rectangle to a OpenCV-style bounding box
                        # [i.e., (x, y, w, h)], then draw the face bounding box

                        # loop over the (x, y)-coordinates for the facial landmarks
                        # and draw them on the image
                    for (x, y) in shape:
                       cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

                    # show the output image with the face detections + facial landmarks

                cv2.imshow("Output", frame)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break

    cv2.destroyAllWindows()


def load_new(name, label):
    if name in FaceVal.subjects:
        # remove all occurrences of the label from the array
        Global.path = 'user_info/'+name+'_'+str(label)
        # Train.labels = list(filter(lambda a: a != label, numpy.array(Train.labels)))
        # Train.faces = list(filter(lambda a: a !=))
    else:
        FaceVal.subjects.append(name)
        VideoDetection.prepare_user(name + "_" + str(label))
    face_recognizer.train(Train.faces, numpy.array(Train.labels))
    print(FaceVal.subjects)
    print('data prepared')
    print('total faces:', len(Train.faces))
    print('total labels:', Train.labels)
    img = FaceDetection.facecrop(FaceDetection.capture_img())
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    FaceVal.label = VideoDetection.predict(gray, face_recognizer)
    print(FaceVal.label)
    Global.monitor_thread = threading.Thread(target=monitor)
    Global.monitor_thread.setDaemon(True)
    Global.monitor_thread.start()


def detect_user(vid):
    img = FaceDetection.facecrop(FaceDetection.capture_img())
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    FaceVal.label = VideoDetection.predict(gray, face_recognizer)
    print(FaceVal.label)