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
start_date=datetime.datetime(2013,5,25,0,0,0,tzinfo=pytz.timezone('Asia/Kolkata'))
matplotlib.rcParams.update({'font.size': 32})

num_days=61
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
	query='select timestamp from smart_meter_data where timestamp between %d and %d;' %(start_timestamp,end_timestamp)
	result=psql.frame_query(query,mysql_conn)
	times=result.values.flatten()
	delta_times=np.diff(times)
	print delta_times,start_date
	if len(delta_times)==0:
		stats['electricity'].append(0)
	else:
		stats['electricity'].append((np.sum(delta_times[delta_times>100])+times[0]-start_timestamp+end_timestamp-times[-1])/3600.0)

print np.mean(stats['electricity'])
#plt.bar(stats['X'],stats['electricity'],color='r')
plt.bar(stats['X'],stats['electricity'])
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d\n%b"))
plt.title('Power outage in hours per day')
plt.ylabel('Hours')

fig=plt.gcf()
fig.set_size_inches(16,9)	
plt.savefig('electricity.png',dpi=100,bbox_inches='tight')
