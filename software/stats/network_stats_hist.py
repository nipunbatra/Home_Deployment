'''This script finds the total number of entries in a day for network pings'''


import pandas as pd
import numpy as np
import MySQLdb
import pandas.io.sql as psql
mysql_conn=MySQLdb.connect(user='root',passwd='password',db='sys_info');
import datetime
import time
import pytz
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib
	
matplotlib.rcParams.update({'font.size': 32})
import json
s = json.load( open("bmh_matplotlibrc.json") )
matplotlib.rcParams.update(s)

start_date=datetime.datetime(2013,5,25,0,0,0,tzinfo=pytz.timezone('Asia/Kolkata'))

num_days=61
stats={}
stats['X']=[]
stats['count']=[]
stats['loss']=[]
stats['ratio']=[]
	
for i in range(num_days):
   	start=start_date+datetime.timedelta(i)
   	end=start_date+datetime.timedelta(i+1)
   	start_timestamp=int(time.mktime(start.timetuple()))
   	end_timestamp=int(time.mktime(end.timetuple()))
	query='select count(*) from sys_info_data where client_id=100 and server_time between %d and %d;' %(start_timestamp,end_timestamp)
 	result=psql.frame_query(query,mysql_conn)
	stats['count'].append(result.values[0][0])
	stats['X'].append(start)
	query='select count(*) from sys_info_data where client_id=100 and packet_loss>0 and server_time between %d and %d;' %(start_timestamp,end_timestamp)
	result=psql.frame_query(query,mysql_conn)
	stats['loss'].append(result.values[0][0])
	if stats['loss'][-1]==0:
		stats['ratio'].append(0)
	else:
		stats['ratio'].append(100.0*stats['loss'][-1]/stats['count'][-1])


sum=0
count=0
for x in stats['ratio']:
	if x>0:
		sum=sum+x
		count=count+1

print sum*1.0/count
	#print stats['loss'],stats['count'],start_timestamp
'''
ax=plt.subplot(3,1,1)
plt.bar(stats['X'],stats['count'],color='r')

plt.title('Packets sent')
plt.subplot(3,1,2,sharex=ax)
plt.bar(stats['X'],stats['loss'],color='g')
plt.title('Number of packets lost')
plt.subplot(3,1,3,sharex=ax)
'''
print len(stats['ratio'])
print stats['ratio']
x=[y for y in stats['ratio'] if y>0]
plt.hist(x,cumulative=True)
plt.title('% packet loss distribution')
plt.ylabel('# days')
plt.xlabel('% packet loss')

#plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d\n%b"))

#plt.show()
fig=plt.gcf()
fig.set_size_inches(16,9)	
plt.savefig('network_hist.png',dpi=100,bbox_inches='tight')
