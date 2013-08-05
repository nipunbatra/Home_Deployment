'''This script finds the total number of entries in a day for smart meter'''


import pandas as pd
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

num_days=55
stats={}
stats['X']=[]
stats['count']=[]
stats['W1']=[]
stats['W2']=[]
	
for i in range(num_days):
   	start=start_date+datetime.timedelta(i)
   	end=start_date+datetime.timedelta(i+1)
   	start_timestamp=int(time.mktime(start.timetuple()))
   	end_timestamp=int(time.mktime(end.timetuple()))
	query='select count(*) from smart_meter_data where timestamp between %d and %d;' %(start_timestamp,end_timestamp)
 	result=psql.frame_query(query,mysql_conn)
 	print result
	stats['count'].append(result.values[0][0])
	stats['X'].append(start)
	query='select avg(W1) from smart_meter_data where timestamp between %d and %d;' %(start_timestamp,end_timestamp)
	result=psql.frame_query(query,mysql_conn)
	if result.values[0][0] is not None:
		stats['W1'].append(result.values[0][0])
	else:
		stats['W1'].append(0)
	query='select avg(W2) from smart_meter_data where timestamp between %d and %d;' %(start_timestamp,end_timestamp)
	result=psql.frame_query(query,mysql_conn)
	if result.values[0][0] is not None:
		stats['W2'].append(result.values[0][0])
	else:
		stats['W2'].append(0)
		
	
		
plt.clf()
plt.subplot(3,1,1)
plt.bar(stats['X'],stats['count'])
plt.title("Number of points")
plt.subplot(3,1,2)
plt.bar(stats['X'],stats['W1'])
plt.title("Average active power for W1")
plt.ylabel('Average Active Power (W)')
plt.subplot(3,1,3)
plt.bar(stats['X'],stats['W2'])
plt.title("Average active power for W2")
plt.ylabel('Average Active Power (W)')
fig = plt.gcf()
fig.set_size_inches(12,10)	
plt.savefig('smart_meter_stats.png',dpi=100)
	
	#time.sleep(2)
	

