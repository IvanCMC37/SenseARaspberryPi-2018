#!/usr/bin/env python3
import sqlite3 as lite

# Database details
dbname='/home/pi/SenseARaspberryPi/db/database.bieber'

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

displayData()