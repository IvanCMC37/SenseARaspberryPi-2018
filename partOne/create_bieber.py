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
    time = datetime.now().strftime("%D")
    print(time)
    cur.execute("INSERT INTO SENSEHAT_data values(?, ?, ?)", ('08/14/18', 34, 55))
    cur.execute("INSERT INTO SENSEHAT_data values(?, ?, ?)", ('08/15/18', 12, 35))
    cur.execute("INSERT INTO SENSEHAT_data values(?, ?, ?)",  ('08/16/18', 18, 41))
    cur.execute("INSERT INTO SENSEHAT_data values(?, ?, ?)",  ('08/17/18', 22, 48))
    cur.execute("INSERT INTO SENSEHAT_data values(?, ?, ?)",  ('08/17/18', 26, 67))
    cur.execute("INSERT INTO SENSEHAT_data values(?, ?, ?)",  (time, 26, 67))
