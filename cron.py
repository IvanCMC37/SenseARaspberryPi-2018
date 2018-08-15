#!/usr/bin/env python3
from crontab import CronTab
    
#init cron
cron = CronTab(user='pi')
cron.remove_all()

#add new cron job
job_1  = cron.new(command='/home/pi/SenseARaspberryPi/partOne.py')
job_2 = cron.new(command='/home/pi/SenseARaspberryPi/partTwo.py')

#job settings
job_1.minute.every(1)
#print("you entered a cron job")
job_2.minute.every(3)
cron.write()