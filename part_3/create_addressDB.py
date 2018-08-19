#!/usr/bin/env python3
import sqlite3 as lite
import sys

#create database for storing known devices
con = lite.connect('/home/pi/SenseARaspberryPi/db/known_devices.db')

with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS ADDRESS_data")
    cur.execute("CREATE TABLE ADDRESS_data(name text, device_name text, mac_address text)")