from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
import sys

#Set Warnings to False
GPIO.setwarnings(False)

#RFID Object Creation
reader = SimpleMFRC522()


#Set up Servo Motor 
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT)

pwm=GPIO.PWM(3,50)
pwm.start(0)


#Define the Function for opening the door
def SetAngle(angle):
    duty=angle/18 +2
    GPIO.output(3,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3,False)
    pwm.ChangeDutyCycle(0)

SetAngle(90)

doorUnlocked = False
prevTime = 0
#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "/home/pi/Desktop/FaceRecognition/encodings2.pickle"
#use this xml file
#https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
cascade = "/home/pi/Desktop/FaceRecognition/haarcascade_frontalface_default.xml"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector..")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)

# initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

try:
    while True:
        
        print("Please verify NFC Tag")
    
        id, text = reader.read()

        if id==78164335817:



            # loop over frames from the video file stream
            while True:
                # grab the frame from the threaded video stream and resize it
                # to 500px (to speedup processing)
                frame = vs.read()
                frame = cv2.flip(frame,-1)
                frame = imutils.resize(frame, width=500)
                
                #Input Frame convertion to GrayScale and RGB for further processing
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # detect faces in the grayscale frame
                rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                    minNeighbors=5, minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE)

                # OpenCV returns bounding box coordinates in (x, y, w, h) order
                # but we need them in (top, right, bottom, left) order, so we
                # need to do a bit of reordering
                boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

                # compute the facial embeddings for each face bounding box
                encodings = face_recognition.face_encodings(rgb, boxes)
                names = []

                # loop over the facial embeddings
                for encoding in encodings:
                    # attempt to match each face in the input image to our known
                    # encodings
                    matches = face_recognition.compare_faces(data["encodings"],
                        encoding)
                    name = "Unknown" #if face is not recognized, then print Unknown
                    
                    
                    # check to see if we have found a match
                    if True in matches:
                        # find the indexes of all matched faces then initialize a
                        # dictionary to count the total number of times each face
                        # was matched
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}
                        

                        if doorUnlocked==False:
                            #Door Open Using Servo
                            SetAngle(180)
                            prevTime = time.time()
                            doorUnlocked=True
                            print("Door Unlocked")


                        # loop over the matched indexes and maintain a count for
                        # each recognized face
                        for i in matchedIdxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1

                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)
                        
                        #If someone in your dataset is identified, print their name on the screen
                        if currentname != name:
                            currentname = name
                            print('Hello! '+currentname)
                    
                    # update the list of names
                    names.append(name)
                    
                
                
                # loop over the recognized faces
                for ((top, right, bottom, left), name) in zip(boxes, names):
                    # draw the predicted face name on the image – color is in BGR
                    cv2.rectangle(frame, (left, top), (right, bottom),
                        (0, 255, 0), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        .8, (0, 255, 0), 3)
                    
                    
                # display the image to our screen
                cv2.imshow("Facial Recognition is Running", frame)
                
                
                if doorUnlocked == True and time.time() - prevTime > 5:
                    cv2.destroyAllWindows()
                    doorUnlocked = False
                    UnlockTime=0
                    SetAngle(90)
                    print('Door Locked')
                    break

                key = cv2.waitKey(1) & 0xFF
                # quit when 'q' key is pressed
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    vs.stop()
                    pwm.stop()
                    GPIO.cleanup()
                    break

                
        
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    vs.stop()
    pwm.stop()
    GPIO.cleanup()
    sys.modules[__name__].__dict__.clear()
