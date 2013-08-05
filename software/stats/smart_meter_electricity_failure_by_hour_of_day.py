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
start_date=datetime.datetime(2013,5,25,0,0,0,tzinfo=pytz.timezone('Asia/Kolkata'))
import matplotlib
matplotlib.rcParams.update({'font.size': 32})

num_days=61
stats={}
stats['X']=[]
stats['count']=[]
stats['electricity']=[]

hours=[None]*24
for i in range(24):
	hours[i]=0

	
for i in range(num_days):
   	start=start_date+datetime.timedelta(i)
   	plt.axvline(start)
   	end=start_date+datetime.timedelta(i+1)
   	print "*"*80
   	print start
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
	idx=delta_times>100
	start_times=times[idx]
	fails=delta_times[delta_times>100]
	if times[0]-start_timestamp>100:
		print "Data missing at start of the day\n"
		print "First datapoint:", datetime.datetime.fromtimestamp(times[0])
		fails=np.insert(fails,0,times[0]-start_timestamp)
		start_times=np.insert(start_times,0,start_timestamp)
	if end_timestamp-times[-1]>100:
		#	print len(fails)
		print "Data missing at end of the day\n"
		print "Last datapoint:", datetime.datetime.fromtimestamp(times[-1])
		fails=np.insert(fails,len(fails),end_timestamp-times[-1])
		start_times=np.insert(start_times,len(start_times),times[-1])
		
	print [datetime.datetime.fromtimestamp(z) for z in start_times]
	#print fails
	'''Finding hour where there was no electricity'''
	h=set()
	for i in range(len(fails)):
		for j in range(start_times[i],start_times[i]+fails[i]):
			h.add(datetime.datetime.fromtimestamp(j).hour)
	
	#print h	
	for ho in h:
		print "Appending count for %d" %ho
		hours[ho]=hours[ho]+1
		plt.scatter(start,ho,s=50)
	#print hours
	
	
	if len(delta_times)==0:
		stats['electricity'].append(0)
	else:
		stats['electricity'].append((np.sum(delta_times[delta_times>100])+times[0]-start_timestamp+end_timestamp-times[-1])/3600.0)

for i in range(24):
	plt.axhline(i)
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d\n%b"))
plt.ylim((-0.5,23.5))
plt.show()
'''
plt.bar(range(24),hours)
plt.xlabel('Hour')
plt.ylabel('# instances')
plt.title('Power outage distribution by hour of day')
plt.xlim((0,23))
fig=plt.gcf()
fig.set_size_inches(16,9)	
plt.savefig('outage_by_hour.png',dpi=100,bbox_inches='tight')
'''
