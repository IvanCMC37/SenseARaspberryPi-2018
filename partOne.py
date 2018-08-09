# In part one we will read temperature and humidity
# We will record in the DB temperature, humidity, time of day and date

from sense_hat import SenseHat
from datetime import datetime
import os, sys

# References to calibrate temp http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
# https://www.raspberrypi.org/forums/viewtopic.php?f=104&t=111457
def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)

sense = SenseHat()
temp = sense.get_temperature()
cpuTemp = get_cpu_temp()
temp_calibrated = temp - ( (cpuTemp - temp) / 2 ) 
# finalTemp = str(temp_calibrated)
# sense.show_message(finalTemp)
print(round(temp_calibrated, 2))