'''This script finds the total number of entries in a day for smart meter'''


import pandas as pd
import numpy as np
import MySQLdb
import pandas.io.sql as psql
mysql_conn=MySQLdb.connect(user='root',passwd='password',db='smart_meter');
import datetime
import time
import pytz
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib
start_date=datetime.datetime(2013,5,29,0,0,0,tzinfo=pytz.timezone('Asia/Kolkata'))
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
   	end_timestamp=int(time.mktime(end.timetuple()))
	query='select count(*) from smart_meter_data where timestamp between %d and %d;' %(start_timestamp,end_timestamp)
 	result=psql.frame_query(query,mysql_conn)
	stats['count'].append(result.values[0][0])
	stats['X'].append(start)
	query='select timestamp,VLN from smart_meter_data where timestamp between %d and %d;' %(start_timestamp,end_timestamp)
	result=psql.frame_query(query,mysql_conn)
	freq=result['VLN'].flatten().values
	x=result['timestamp'].flatten().values
	times=[datetime.datetime.fromtimestamp(y) for y in x]
plt.plot(times,freq)
plt.title('Voltage vs Time')
plt.xlabel('Time')
plt.ylabel('Voltage (V)')
plt.grid()
plt.axhline(230,linewidth=3)
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H\nhrs"))
fig=plt.gcf()
fig.set_size_inches(16,9)	
plt.savefig('voltage.png',dpi=100,bbox_inches='tight')
