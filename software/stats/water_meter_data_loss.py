'''This script finds the total number of entries in a day for smart meter'''


import pandas as pd
import numpy as np
import MySQLdb
import pandas.io.sql as psql
mysql_conn_1=MySQLdb.connect(user='root',passwd='password',db='water');
mysql_conn=MySQLdb.connect(user='root',passwd='password',db='smart_meter');

import datetime
import time
import pytz
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib
start_date=datetime.datetime(2013,7,15,0,0,0,tzinfo=pytz.timezone('Asia/Kolkata'))
matplotlib.rcParams.update({'font.size': 32})

num_days=14
stats={}
stats['X']=[]
stats['count']=[]
stats['water_count']=[]

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
		stats['electricity'].append((np.sum(delta_times[delta_times>30])+times[0]-start_timestamp+end_timestamp-times[-1]))
	query='select count(*) from water_data where meter_id=1 and timestamp between %d and %d;' %(start_timestamp,end_timestamp)
	result=psql.frame_query(query,mysql_conn_1)
	query='select timestamp from water_data where meter_id=1 and timestamp between %d and %d;' %(start_timestamp,end_timestamp)
	result=psql.frame_query(query,mysql_conn_1)
	times_water=result.values.flatten()
	h=set()
	for time_ in times_water:
		h.add(int(time_))
	stats['water_count'].append(len(h))
	
	
#stats['water']=[x/1.0 for x in  stats['water_count']]
print np.mean(stats['electricity'])
#plt.bar(stats['X'],stats['electricity'],color='r')
#stats['software']=86400*np.ones(len(stats['electricity']))-stats['electricity']-stats['count']

#plt.bar(stats['X'],stats['count'])
#plt.bar(stats['X'],stats['electricity'],bottom=stats['count'],color='r')
#plt.bar(stats['X'],stats['software'],bottom=stats['electricity']+stats['count'],color='g')

#plt.axhline(86400,linewidth=20,color='g')
#plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d\n%b"))
#plt.title('Power outage in hours per day')
#plt.ylabel('Hours')
#plt.show()
#plt.clf()
print stats['water_count']
stats['missing']=[]
stats['bottom']=[]


for i in range(len(stats['water_count'])):
	if stats['water_count'][i]+stats['electricity'][i]>86400:
		stats['electricity'][i]=86400-stats['water_count'][i]
		stats['missing'].append(0)
		stats['bottom'].append(86400)
	else:
		stats['missing'].append(86400-stats['water_count'][i]-stats['electricity'][i])
		stats['bottom'].append(stats['water_count'][i]+stats['electricity'][i])



print stats['bottom']
print stats['missing']
plt.bar(stats['X'],stats['water_count'],label='Collected data')
plt.bar(stats['X'],stats['electricity'],bottom=stats['water_count'],color='r',label='Power outage')
plt.bar(stats['X'],stats['missing'],bottom=stats['bottom'],color='g',label='Software loss')
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d\n%b"))
plt.ylim((80000,87000))
#plt.legend()
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
      ncol=1, mode="expand", borderaxespad=0.)
plt.ylabel('Points')
fig=plt.gcf()
fig.set_size_inches(16,9)	
plt.savefig('data_loss.png',dpi=100,bbox_inches='tight')

