#!/usr/bin/env python3
import os
import sqlite3 as lite
from datetime import datetime as dt
from flask import Flask, request, render_template
import numpy as np
import matplotlib
# dont use windows backend by default
matplotlib.use('Agg')
from matplotlib import pyplot as plt 

app = Flask(__name__, template_folder='views')
dbname = '/home/pi/SenseARaspberryPi/db/database.bieber'

@app.route("/")
def plotTemp():
    conn=lite.connect(dbname)
    curs=conn.cursor()
    curs.execute("SELECT temp FROM SenseHat_data")
    tempData = curs.fetchall()
    curs.execute("SELECT timestamp FROM SenseHat_data")
    dates = curs.fetchall()
    xdates = [dt.strptime('{2:7}'.format(str(d)),'%d%m%y') for d in dates]

    plt.figure()
    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.plot(xdates,tempData)
    plt.ylabel('Temperature (C)')
    plt.xlabel('Date')
    plt.savefig('static/temp.png')
    conn.close()
    return render_template('temp.html', temp = "static/temp.png")

@app.route("/humid")
def plotHumid():
    conn=lite.connect(dbname)
    curs=conn.cursor()
    curs.execute("SELECT humidity FROM SenseHat_data")
    humidData = curs.fetchall()

    plt.figure()
    plt.plot(humidData)
    plt.ylabel('humidity (%)')
    plt.savefig('static/humid.png')
    #mayeb try as an array
    return render_template('humid.html', humid = "static/humid.png")
    

host = os.popen('hostname -I').read()
#port set to a non privileged port above 1024
app.run(host='192.168.1.4', port=5000, debug=False)