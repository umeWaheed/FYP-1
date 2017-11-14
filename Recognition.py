import cv2
import sys
import os
import numpy

# Get user supplied values
#imagePath = "training_data\index.jpg"


def detect_face(image):
    cascpath = "C:\\Users\\ACER\\Downloads\\opencv\\sources\\data\\lbpcascades\\lbpcascade_frontalface.xml"

    facecascade = cv2.CascadeClassifier(cascpath)

    # Read the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = facecascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=2,
        minSize=(20, 20),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces)==0:
        print('none')
        return None,None
    #else:
        #print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    (w,x,y,h) = faces[0]
    return gray[y:y+w,x:x+h],faces[0]


def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)

    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []

    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue
        label = int(dir_name.replace("s", ""))

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

            cv2.imshow("Training on image...", image)
            cv2.waitKey(100)
            # detect face
            face, rect = detect_face(image)

            if face is not None:
                faces.append(face)
                labels.append(label)

    cv2.destroyAllWindows()
    cv2.waitKey(100)
    cv2.destroyAllWindows()
    return faces, labels


def draw_rectangle(img, rect):
 (x, y, w, h) = rect
 cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)


def draw_text(img,text,x,y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


def predict(test_img):
    # make a copy of the image as we don't want to change original image
    img = test_img.copy()
    # detect face from the image
    face, rect = detect_face(img)

    # predict the image using our face recognizer
    label,confidence = face_recognizer.predict(face)
    # get name of respective label returned by face recognizer
    label_text = subjects[label]

    # draw a rectangle around face detected
    draw_rectangle(img, rect)
    # draw name of predicted person
    draw_text(img, label_text, rect[0], rect[1] - 5)

    return img


subjects=["none","emma","not emma"]
print('preparing data...')
faces,labels = prepare_training_data("training_data")
print('data prepared')
print('total faces:',len(faces))
print('total labels:',labels)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces,numpy.array(labels))

print("Predicting images...")

# load test images
test_img1 = cv2.imread("test_data/index.jpg")
test_img2 = cv2.imread("test_data/index2.jpg")

# perform a prediction
predicted_img1 = predict(test_img1)
predicted_img2 = predict(test_img2)
print("Prediction complete")

# display both images
cv2.imshow(subjects[0], predicted_img1)
cv2.imshow(subjects[1], predicted_img2)
cv2.waitKey(0)
cv2.destroyAllWindows()