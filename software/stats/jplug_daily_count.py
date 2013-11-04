d'''This script finds the total number of entries in a day for each jplug
and optionallty can also plot and save the same'''


import pandas as pd
import MySQLdb
import pandas.io.sql as psql
mysql_conn=MySQLdb.connect(user='root',passwd='password',db='jplug');
import datetime
import time
import pytz
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
start_date=datetime.datetime(2013,5,28,0,0,0,tzinfo=pytz.timezone('Asia/Kolkata'))
jplug_ids=["001EC00CC4A0","001EC00CC4A1","001EC00CC4AD","001EC00CC49C","001EC00CC49F","001EC00D7A18","001EC00CC49D","001EC00D7A1D","001EC00D7A1C"]
jplug_ids=["001EC00CC4A0"]
num_days=61
stats={}
for jplug in jplug_ids:
	stats[jplug]={}
	stats[jplug]['X']=[]
	stats[jplug]['count']=[]
	stats[jplug]['mean']=[]
	stats[jplug]['max']=[]
	stats[jplug]['min']=[]
	for i in range(num_days):
 	   	start=start_date+datetime.timedelta(i)
 	   	end=start_date+datetime.timedelta(i+1)
 	   	start_timestamp=int(time.mktime(start.timetuple()))
 	   	end_timestamp=int(time.mktime(end.timetuple()))
		query='select count(*) from jplug_data where mac="%s" and timestamp between %d and %d;' %(jplug,start_timestamp,end_timestamp)
 	   	result=psql.frame_query(query,mysql_conn)
		stats[jplug]['count'].append(result.values[0][0])
		stats[jplug]['X'].append(start)
		query='select avg(active_power) from jplug_data where mac="%s" and timestamp between %d and %d;' %(jplug,start_timestamp,end_timestamp)
		result=psql.frame_query(query,mysql_conn)
		#print result
		if result.values[0][0] is not None:
                	stats[jplug]['mean'].append(result.values[0][0])
                else:
			stats[jplug]['mean'].append(0)
		#stats[jplug]['X'].append(start)
	
		
	plt.clf()
	plt.subplot(2,1,1)
	plt.bar(stats[jplug]['X'],stats[jplug]['count'])
	plt.title("Number of points for %s" %jplug)
	plt.subplot(2,1,2)
	plt.bar(stats[jplug]['X'],stats[jplug]['mean'])
	plt.title("Average active power for %s" %jplug)
	plt.ylabel('Average Active Power (W)')
	fig = plt.gcf()
	fig.set_size_inches(12,10)	
	plt.savefig('%s.png' %jplug,dpi=100)
	
	#time.sleep(2)
	

