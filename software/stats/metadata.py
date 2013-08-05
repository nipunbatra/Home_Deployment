'''This script finds the total number of entries in a day for smart meter'''


import pandas as pd
import numpy as np
import MySQLdb
import pandas.io.sql as psql
mysql_conn=MySQLdb.connect(user='root',passwd='password',db='jplug');
import datetime
import time
import pytz
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib
start_date=datetime.datetime(2013,7,5,0,0,0,tzinfo=pytz.timezone('Asia/Kolkata'))
matplotlib.rcParams.update({'font.size': 32})

num_days=1
stats={}
stats['X']=[]
stats['count']=[]
stats['electricity']=[]
	
for i in range(num_days):
   	start=start_date+datetime.timedelta(i)
   	end=start_date+datetime.timedelta(i+1)
   	start_timestamp=int(time.mktime(start.timetuple()))
   	end_timestamp=start_timestamp+6*60*60
	query='select timestamp,active_power from jplug_data where mac= "001EC00CC4A0" and timestamp between %d and %d;' %(start_timestamp,end_timestamp)
	result=psql.frame_query(query,mysql_conn)
	freq=result['active_power'].flatten().values
	x=result['timestamp'].flatten().values
	times=[datetime.datetime.fromtimestamp(y) for y in x]
plt.plot(times,freq)
plt.title('Active Power vs Time for refrigerator')
plt.xlabel('Time')
plt.ylabel('Active Power (W)')
plt.grid()
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H\nhrs"))
fig=plt.gcf()
fig.set_size_inches(16,9)	
plt.savefig('after_repair.png',dpi=100,bbox_inches='tight')

