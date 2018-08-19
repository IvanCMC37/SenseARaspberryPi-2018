#!/usr/bin/env python3
import bluetooth
import sqlite3 as lite
import os
import time
from sense_hat import SenseHat

# Writing to Database
dbname='/home/pi/SenseARaspberryPi/known_devices.db'
sampleFreq = 1 # time in seconds

# log sensor data on database
def logData (name, device_name, mac_address):	
    conn=lite.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO ADDRESS_data values(?, ?, ?)", (name, device_name, mac_address))
    conn.commit()
    conn.close()

# display database data
def displayData():
    conn=lite.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    print('{:20}{:20}{:20}'.format("name","device_name","mac_address"))
    for x in curs.execute("SELECT * FROM ADDRESS_data"):
        #extracting mac_address object
        s = str(x)
        mac_address = s[2:len(s)-3]

        # string formatting
        a,b,c = s.split(",")
        name = a[2:len(a)-1]
        device_name = b[2:len(b)-1]
        mac_address = c[2:len(c)-2]
        print('{:20}{:20}{:20}'.format(name,device_name,mac_address))

    #print(a[2:len(a)-1] +" "+str(len(a[2:len(a)-1])))
    #print(b[2:len(b)-1]+" "+str(len(b[2:len(b)-1])))
    #print(c[2:len(c)-2]+" "+str(len(c[2:len(c)-2])))

    #print(curs.execute("SELECT mac_address FROM ADDRESS_data"))
    conn.close()

def checkTotalRow():
    conn=lite.connect(dbname)
    curs=conn.cursor()
    row_count = curs.execute("SELECT COUNT(*) FROM ADDRESS_data")
    value = row_count.fetchone()
    conn.close()
    return value[0]

# check if the "new" mac address was in the db or not
def checkDuplication(user_name, device_name,input_address):
    print("Checking for duplication..")
    conn=lite.connect(dbname)
    curs=conn.cursor()
    #print ("\nEntire database contents:\n")
    #print("name     device name    mac_address")
    for x in curs.execute("SELECT mac_address FROM ADDRESS_data"):
        #extracting mac_address object
        s = str(x)
        mac_address = s[2:len(s)-3]

        #check if the mac address exists in the current database
        if(mac_address==input_address):
            print("The device you were trying to add is already in the database...")
        else:
            logData(user_name, device_name, input_address)
            print("New device "+mac_address+" added.")
        
    if(checkTotalRow()==0):
        print("First row added")
        logData(user_name, device_name, input_address)
        displayData()
    
    if(checkTotalRow()>0):    
        displayData()
    
    conn.close()
    print("ended check")

# Main function
def main():
    user_name = input("Enter your name: ")
    device_name = input("Enter the name of your phone: ")
    search(user_name, device_name)

# Search for device based on device's name
def search(user_name, device_name):
    quit_check = False
    fail_count = 0
    while True:
        device_address = None
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        time.sleep(3) #Sleep three seconds 
        nearby_devices = bluetooth.discover_devices()

        for mac_address in nearby_devices:
            if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                device_address = mac_address
                break
        if device_address is not None:
            checkDuplication(user_name, device_name, device_address)
            print("Hi {}! Your phone ({}) has the MAC address: {}".format(user_name, device_name, device_address))
            sense = SenseHat()
            temp = round(sense.get_temperature(), 1)
            sense.show_message("Hi {}! Current Temp is {}*c".format(user_name, temp), scroll_speed=0.05)
            quit_check = True
        else:
            fail_count += 1
            print("Could not find target device nearby...")
        
        if(fail_count>=3):
            print("Failed to find target device more than 3 times, ending the program...")
            break
        elif(quit_check==True):
            break

        
        

#Execute program
main()
