#!/usr/bin/env python3
from sense_hat import SenseHat
from datetime import datetime
import sqlite3 as lite
import os, sys, time
from time import sleep

# In part one we will read temperature and humidity
# We will record in the DB temperature, humidity, time of day and date

# References to calibrate temp http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
# https://www.raspberrypi.org/forums/viewtopic.php?f=104&t=111457
def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)

# Writing to Database
dbname='/home/pi/SenseARaspberryPi/db/database.bieber'
sampleFreq = 1 # time in seconds

# get data from SenseHat sensor
def getSenseHatData():	
    # Read temperature
    sense = SenseHat()
    temp = sense.get_temperature()
    cpuTemp = get_cpu_temp()
    temp_calibrated = temp - ( (cpuTemp - temp) / 2 ) 

    # Read Humidity
    humidity = sense.get_humidity()
	
    if temp_calibrated is not None and humidity is not None:
        temp_calibrated = round(temp_calibrated, 2)
        humidity = round(humidity, 2)
        time = datetime.now().strftime("%D %H:%M")
        logData (temp_calibrated, humidity, time)

# log sensor data on database
def logData (temp, humidity, time):	
    conn=lite.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO SENSEHAT_data values(?, ?, ?)", (time, temp, humidity))
    conn.commit()
    conn.close()

# display database data
def displayData():
    conn=lite.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    print("DateTime     Temperature (C)    Humidity (%)")
    for row in curs.execute("SELECT * FROM SenseHat_data"):
        print (row)
    conn.close()

# main function
def main():
    sense = SenseHat()
    red = (255, 0, 0)
    sense.clear(red)  # passing in an RGB tuple
    

    for i in range (0,3):
        getSenseHatData()
        time.sleep(sampleFreq)
    displayData()
    sense.clear()

# Execute program 
main()


#table is datetime , temp , humidity