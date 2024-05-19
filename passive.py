import base64
import requests

import cv2
import numpy as np

from gtts import gTTS
import os

import speech_recognition as sr

import threading
import queue
import time
from pathlib import Path
from openai import OpenAI

import subprocess


#openai
api_key = ""
client = OpenAI(api_key=api_key)
#init

# OpenAI API Key

cv2.namedWindow("test")



r = sr.Recognizer() 

img_counter = 0

classes = ["background", "person", "bicycle", "car", "motorcycle",
  "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
  "unknown", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
  "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "unknown", "backpack",
  "umbrella", "unknown", "unknown", "handbag", "tie", "suitcase", "frisbee", "skis",
  "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
  "surfboard", "tennis racket", "bottle", "unknown", "wine glass", "cup", "fork", "knife",
  "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
  "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "unknown", "dining table",
  "unknown", "unknown", "toilet", "unknown", "tv", "laptop", "mouse", "remote", "keyboard",
  "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "unknown",
  "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush" ]


colors = np.random.uniform(0, 255, size=(len(classes), 3))
pb  = 'frozen_inference_graph.pb'
pbt = 'ssd_inception_v2_coco_2017_11_17.pbtxt'
cvNet = cv2.dnn.readNetFromTensorflow(pb,pbt)   



cam = cv2.VideoCapture(0)

ret, img = cam.read()


def opentts(text):
    
  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input=text
  )

  response.stream_to_file(speech_file_path) 
  subprocess.run(["afplay", "speech.mp3"])



def main():

    timer = 0
    cam = cv2.VideoCapture(0)



    while True:
        timer+=1

        pplleft = 0
        pplright = 0
        pplfront = 0

        ret, img = cam.read()

        rows = img.shape[0]
        cols = img.shape[1]
        cvNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))

        cvOut = cvNet.forward()


        for detection in cvOut[0,0,:,:]:
          score = float(detection[2])
          if score > 0.3:

            idx = int(detection[1])   # prediction class index. 

            
               

            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows

            if(classes[idx] == "person"):
                if(left < 300):
                    pplleft+=1
                elif(left > 700):
                    pplright+=1
                else:
                    pplfront+=1
                
                  

            cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)
                

            label = "{}: {:.2f}%".format(classes[idx],score * 100)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(img, label, (int(left), int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 2)
        cv2.imshow('my webcam', img)

        if(timer > 50):

            talk = "there are "
            if(pplleft == 0 and pplright == 0 and pplfront ==0):
                talk += "no people I can see!"
            if(pplleft>1):
                talk += str(pplleft)+" people to your left!"
            if(pplright>1):
                talk += str(pplright)+" people to your right!"
            if(pplfront>1):
                talk += str(pplfront)+" people in front of you!"

            if(pplleft==1):
                talk += str(pplleft)+" person to your left!"
            if(pplright==1):
                talk += str(pplright)+" person to your right!"
            if(pplfront==1):
                talk += str(pplfront)+" person in front of you!"

            print("pplleft: ", pplleft, ". ppl right: ", pplright, ". ppl front: ", pplfront)
            
            opentts(talk)
            timer = 0


        if not ret:
            print("failed to grab frame")
            break

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        time.sleep(0.01) 

if (__name__ == '__main__'): 
    main()





cam.release()

cv2.destroyAllWindows()
