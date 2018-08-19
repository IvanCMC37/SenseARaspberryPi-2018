#!/usr/bin/env python3
import sqlite3 as lite
import sys

#create database for storing readings
con = lite.connect('/home/pi/SenseARaspberryPi/db/database.bieber')

with con: 
    curs= con.cursor() 
    curs.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    curs.execute("CREATE TABLE SENSEHAT_data(timestamp DATETIME, temp REAL, humidity REAL)")