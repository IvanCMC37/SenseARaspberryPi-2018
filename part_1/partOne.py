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

# Database details
dbname='/home/pi/SenseARaspberryPi/db/database.bieber'
sampleFreq = 1 # time in seconds

# function to get cpu temperature
def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)

# get data from SenseHat sensor
def getSenseHatData():	
    sense = SenseHat()

    # Read temperature
    temp = sense.get_temperature()
    cpuTemp = get_cpu_temp()
    temp_calibrated = temp - ( (cpuTemp - temp) / 2 ) 

    # Read Humidity
    humidity = sense.get_humidity()
	
    # making sure no empty data will be added to database table
    if temp_calibrated is not None and humidity is not None:
        temp_calibrated = round(temp_calibrated, 2)
        humidity = round(humidity, 2)
        time = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        logData (temp_calibrated, humidity, time)
        print("New data added to database table @"+time)

# log sensor data on database
def logData (temp, humidity, time):	
    #setting up database connection
    conn=lite.connect(dbname)
    curs=conn.cursor()

    # insert data to table
    curs.execute("INSERT INTO SENSEHAT_data values(?, ?, ?)", (time, temp, humidity))
    conn.commit()

    # close database connection
    conn.close()

# display database data
def displayData():
    # setting up connection
    conn=lite.connect(dbname)
    curs=conn.cursor()

    print ("\nDatabase content as following...\n")
    print('{:20}{:17}{:20}'.format("DateTome","Temperature(C)","Humidity(%)"))

    for x in curs.execute("SELECT * FROM SenseHat_data"):
        #extracting object to string
        s = str(x)

        # string formatting
        a,b,c = s.split(",")
        dateTime = a[2:len(a)-1]
        temperature = b[1:len(b)]
        humidity = c[1:len(c)-1]

        #print the formatted row
        print('{:20}{:17}{:20}'.format(dateTime,temperature,humidity))
       
    #close database connection
    conn.close()

# main function
def main():
    sense = SenseHat()
    red = (255, 0, 0)
    # set SenseHat to red colour to show the script has started
    sense.clear(red)
    
    # get new SenseHat reading
    getSenseHatData()
    displayData()

    # turn off the SenseHat light to show the script has ended
    sense.clear()

# Execute program 
main()