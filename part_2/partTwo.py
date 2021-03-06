#!/usr/bin/env python3
from sense_hat import SenseHat
import requests
import json
import os

print("Assignment part two started...")
#Referencing from tute 4 - pushBullet example
ACCESS_TOKENS = [["o.UPqDVIbmvEuNmjQiNg0IAVkFdFINeB34","Ivan"]]
ACCESS_TOKENS.append(["o.814RKndb4upm5YdPrgIvLb6tm2WWxSpO","David"])
Name_OF_PI = "Ivan's Pi"

#create senseHat object to sense the temperature
sense = SenseHat()
sense.clear()

#fetch the current sensor temperature
senor_temp = sense.get_temperature()

# References to calibrate temp http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
# https://www.raspberrypi.org/forums/viewtopic.php?f=104&t=111457
def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)

#function to decide whether broadcast the message or not
def pushBullet_broadcaster():
    #fetch cpu temp
    cpu_temp = get_cpu_temp()

    #calculating the *real* temp
    temp = senor_temp - (cpu_temp -senor_temp)/2

    # send message when temperature is below 25
    if temp <25:
        for x in ACCESS_TOKENS:
            body = "Hey "+x[1]+", time to get your jacket!!! It's "+str(round(temp,1))+"*C outside."
            data_send = {"type": "note", "title": Name_OF_PI, "body": body}
            resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                            headers={'Authorization': 'Bearer ' + x[0], 
                            'Content-Type': 'application/json'})
            if resp.status_code != 200:
                raise Exception('Failed to reach {}.'.format(x[1]))
            else:
                print('Sent message to {}'.format(x[1]))
        print("All message(s) has been sent.")

#main function
def main():
    pushBullet_broadcaster()

#execute the main function
main()
