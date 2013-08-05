#!/usr/bin/python
import subprocess,sys
import time
import os
import datetime
import random
import glob
#import MySQLdb
import csv
import os
import shutil

from pytz import timezone

a=((int)(time.time()))-3600
PATH = "/root/multisensor"
#os.system("cp "+PATH+"/OZW_Log.txt "+PATH+"/Log/OZW_Log_"+str(HOUR)+"_"+str(MIN))
#print 'File Copied'
while True:
	now = datetime.datetime.now(timezone('Asia/Kolkata'))
	DAY=now.day
	MONTH=now.month
	HOUR=now.hour
	MIN=now.minute
	source_f = PATH+"/OZW_Log.txt"
	dest_f = PATH+"/Log/OZW_Log_"+str(DAY)+"_"+str(MONTH)+"_"+str(HOUR)+"_"+str(MIN)
	shutil.copy(source_f,dest_f)
	time.sleep(1)
	os.chdir(PATH)
	os.system(PATH+"/HomeZwave")
	time.sleep(1)
	
