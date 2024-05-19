import serial
import os

import subprocess
ser = serial.Serial('/dev/cu.usbserial-14140', 9600)



#hold down turns off
#tap it rotates

holdcounter = 0

#false = off
#true = on
onOff = False

#false = passive
#true = active
passAct = True #first turn on is always active

process = None

while True:

    
    data = ser.readline().decode().strip()


    if data=="0":
        holdcounter += 1
        

    if data=="1" and holdcounter != 0: #let go see how long they held
        if(holdcounter>10):
            print(onOff)
            if(onOff == False):
                print("starting")
                os.system("afplay startupnoise.mp3")  
                subprocess.run(["afplay", "greeting.mp3"])
                process = subprocess.Popen(['python3', 'active.py'])
                onOff = True
            else:
                #how to terminate all
                process.terminate()
                onOff = False
            
        else:#cycle modes
            print('cycle')
            if(passAct == True):
                passAct = False #turn to passive mode cv
                process.terminate()
                process = subprocess.Popen(['python3', 'passive.py'])
            else:
                passAct = True #turn to active mode cv
                process.terminate()
                process = subprocess.Popen(['python3', 'active.py'])
            
            
        holdcounter = 0 #reset cause they let go
    



