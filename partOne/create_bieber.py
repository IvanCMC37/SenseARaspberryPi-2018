#!/usr/bin/env python3
import sqlite3 as lite
import sys
import os, sys, time
from datetime import datetime, timedelta

con = lite.connect('/home/pi/SenseARaspberryPi/db/database.bieber')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    cur.execute("CREATE TABLE SENSEHAT_data(timestamp DATETIME, temp REAL, humidity REAL)")
    #test input
    time = datetime.now().strftime("%d%m%y")
    print(time)
    print(len(time))
    print(type(time))

    cur.execute("INSERT INTO SENSEHAT_data values(?, ?, ?)",  (time, 26, 67))
