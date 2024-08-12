

import assemblyai as aai

import os; import appscript; import time

import pyautogui


import cv2
import base64
import requests
import os
import speech_recognition as sr
import numpy as np


from pathlib import Path
from openai import OpenAI

import subprocess




contacts = {
    "call jeremy": "",
    "call victoria": ""
}



#openai
api_key = "sk-proj-6QCfuf00NOEj4B5eT8ELT3BlbkFJEWICNxZofp1H05Ufx7qM"

#assemblyai
aai.settings.api_key = "0b4ddfbf65af49a885ff85ea61576f52"
client = OpenAI(api_key=api_key)

cam = cv2.VideoCapture(0)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def analyzeVideo(prompt):
  global ret, img
  ret, img = cam.read()

  os.remove("picture.png") #reset
  img_name = "picture.png".format(0)

  cv2.imwrite(img_name, img)
  image_name = "picture.png"
  
  base64_image = encode_image(image_name)

  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
  }

  payload = {
      "model": "gpt-4o",
      "messages": [
        {
          "role": "system",
          "content": "You are an AI assistant that talks very human with pauses and stutters that provides concise and helpful responses. You should make any assumptions necessary, keep responses to 2 sentences, and refer to images only if needed."
          },
          {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 70
  }

  
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  print(response)
  content = response.json()["choices"][0]['message']['content']
  return(content)





def on_open(session_opened: aai.RealtimeSessionOpened):
  "This function is called when the connection has been established."

  print("Session ID:", session_opened.session_id)




def on_data(transcript: aai.RealtimeTranscript):
  flag = True
  "This function is called when a new transcript has been received."

  if not transcript.text:
    return

  if isinstance(transcript, aai.RealtimeFinalTranscript):
    print(transcript.text, end="\r\n")


    #reading for command
    if(transcript.text.lower().find("lucky")!=-1):
      subprocess.run(["afplay", "recognized.mp3"])
      for key in contacts:
        if key in (transcript.text.lower()):
          print(contacts[key])
          os.popen('open facetime://' + contacts[key])
          appscript.app('FaceTime').activate() 
          time.sleep(1)
          pyautogui.click(90,750)
          flag = False
      if(flag and transcript.text.lower().find("end the call")!=-1):
        pyautogui.click(250,750)
      elif(flag and transcript.text.lower().find("call 911")!=-1):
        os.system("afplay alarm.mp3")
        os.system("afplay alarmvoice.mp3")

      elif(flag and transcript.text.lower().find("thank you")!=-1):
        os.system("afplay thanks.mp3")
      elif(flag):
        #subprocess.run(["afplay", "loading.mp3"])
        opentts(analyzeVideo(transcript.text.lower()))

      transcript.text = "" #reset the sentence after first check
        
  else:
    print(transcript.text, end="\r")
      



def on_error(error: aai.RealtimeError):
  "This function is called when the connection has been closed."

  print("An error occured:", error)

def on_close():
  "This function is called when the connection has been closed."

  print("Closing Session")

def opentts(text):
    
  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input=text,
  )

  response.stream_to_file(speech_file_path) 
  os.system("afplay speech.mp3")  


transcriber = aai.RealtimeTranscriber(
  on_data=on_data,
  on_error=on_error,
  sample_rate=44_100,
  on_open=on_open, # optional
  on_close=on_close, # optional
)



# Start the connection
transcriber.connect()

# Open a microphone stream
microphone_stream = aai.extras.MicrophoneStream()

# Press CTRL+C to abort
transcriber.stream(microphone_stream)

transcriber.close()
    
  #how do i delete an email on this app
  #what is this thing i am holding (ecg electrodes)

  #assistance using tech/what things do
  #translation (for travel and using stuff (find image or differnet lenguage))
  #how do i delete an email on this app
  #general questions and conversations (pain and emotional help loneliness)

  #visually impaired or blind features
  #describe what I am looking at or how muchmoney you are holdingg
  #passive vs active mode (explain how blind people can use it and tune it to whatever obstacles or people used for an outdoor setting when exploring)

  #specifically say it IS "SUSTAINable" having one of its spikes being extrememly flexible and modular
  #show and quickly explain some of the aditionaly features
  
