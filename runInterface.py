#!/usr/bin/env python3
import os
import sqlite3 as lite
from flask import Flask, request, render_template, send_file
import matplotlib
# dont use windows backend by default
matplotlib.use('Agg')
from matplotlib import pyplot as plt 
import base64, io

app = Flask(__name__, template_folder='views')

@app.route("/")
def plotTemp():
    conn=lite.connect('/home/pi/SenseARaspberryPi/db/database.bieber')
    curs=conn.cursor()
    conn.close()

    plt.figure()
    plt.plot([11,22, 88, 23])
    plt.ylabel('new numbers')
    plt.savefig('static/temp.png')
    return render_template('temp.html', temp = "static/temp.png")

@app.route("/humid")
def plotHumid():
    plt.figure()
    plt.plot([18,28,1,4])
    plt.ylabel('goooy numbers')
    plt.savefig('static/humid.png')
    return render_template('humid.html', humid = "static/humid.png")
    

host = os.popen('hostname -I').read()
#port set to a non privileged port above 1024
app.run(host='192.168.1.4', port=5000, debug=False)