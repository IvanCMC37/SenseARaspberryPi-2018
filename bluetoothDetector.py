#!/usr/bin/env python3
import bluetooth
import sqlite3 as lite
import os
import time
from sense_hat import SenseHat

# database details
dbname='/home/pi/SenseARaspberryPi/known_devices.db'

# log device data on database
def logData (name, device_name, mac_address):	
    conn=lite.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO ADDRESS_data values(?, ?, ?)", (name, device_name, mac_address))
    conn.commit()
    conn.close()

# display database data
def displayData():
    # setting up connection
    conn=lite.connect(dbname)
    curs=conn.cursor()

    print ("\nDatabase content as following...\n")
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

    #close connection
    conn.close()

# function to check total row of the database table
def checkTotalRow():
    conn=lite.connect(dbname)
    curs=conn.cursor()

    row_count = curs.execute("SELECT COUNT(*) FROM ADDRESS_data")
    value = row_count.fetchone()

    conn.close()
    return value[0]

# check if the "new" mac address was in the db or not
def checkDuplication(user_name, device_name,input_address):
    print("Checking for mac_address duplication...")
    conn=lite.connect(dbname)
    curs=conn.cursor()

    for x in curs.execute("SELECT mac_address FROM ADDRESS_data"):
        #extracting mac_address object
        s = str(x)
        mac_address = s[2:len(s)-3]

        #check if the mac address exists in the current database
        if(mac_address==input_address):
            print("The device that you were trying to add was already in the database...\nNo new device is added...")
        else:
            logData(user_name, device_name, input_address)
            print('New device{} - {} - {} added.'.format(user_name, device_name,input_address))
    print("Duplication check ended...")   
     
    # add the new data to table if the current table is empty
    if(checkTotalRow()==0):
        print("Database is empty, adding first row...")
        logData(user_name, device_name, input_address)
        displayData()

    # print database content if the database is not empty
    if(checkTotalRow()>0):    
        displayData()
    
    #close database connection
    conn.close()

# Main function
def main():
    user_name = input("Enter your name: ")
    device_name = input("Enter the name of your phone: ")
    search(user_name, device_name)

# Search for device based on device's name
# modified from tutorial week 5 example
def search(user_name, device_name):
    quit_check = False
    fail_count = 0

    while True:
        device_address = None
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        time.sleep(3) #Sleep three seconds 
        nearby_devices = bluetooth.discover_devices()

        # search all available nearby devices
        for mac_address in nearby_devices:
            # if the mac_address has the device_name that we are looking for, proceed to next part
            if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                device_address = mac_address
                break

        # making sure that mac address is not empty
        if device_address is not None:
            print("Hi {}! Your phone ({}) has the MAC address: {}".format(user_name, device_name, device_address))

            #check if the current database table contains the related device or not, add to table if not.
            checkDuplication(user_name, device_name, device_address)

            #initial SenseHat and send greet to the user
            sense = SenseHat()
            temp = round(sense.get_temperature(), 1)
            print("Greeting on SenseHat...")
            sense.show_message("Hi {}! Current Temp is {}*c".format(user_name, temp), scroll_speed=0.05)

            #end of mission, quit the program after
            quit_check = True
        else:
            #count how many times failling to find the target device
            fail_count += 1
            print("Could not find target device nearby...")
        
        #quit if could not find the target device more than 3 times
        if(fail_count>=3):
            print("Failed to find target device more than 3 times, ending the program...")
            break
        #end of mission quit
        elif(quit_check==True):
            print("Greeting sent, ending the program...")
            break

#Execute program
main()