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

num_days=2
stats={}
stats['X']=[]
stats['count']=[]
stats['electricity']=[]
F=[]
V=[]
for i in range(num_days):
   	start=start_date+datetime.timedelta(i)
   	end=start_date+datetime.timedelta(i+1)
   	start_timestamp=int(time.mktime(start.timetuple()))
   	end_timestamp=int(time.mktime(end.timetuple()))
	query='select count(*) from smart_meter_data where timestamp between %d and %d;' %(start_timestamp,end_timestamp)
 	result=psql.frame_query(query,mysql_conn)
	stats['count'].append(result.values[0][0])
	stats['X'].append(start)
	query='select timestamp,VLN,F from smart_meter_data where timestamp between %d and %d;' %(start_timestamp,end_timestamp)
	result=psql.frame_query(query,mysql_conn)
	v=result['VLN'].flatten().values
	f=result['F'].flatten().values
	F.append(f)
	V.append(v)
FR=[]
VO=[]
for i in range(len(V)):
	for j in range(len(V[i])):
		FR.append(F[i][j])
		VO.append(V[i][j])

	
plt.boxplot(VO)
plt.title('Voltage Boxplot')
plt.ylabel('Voltage (V)')
plt.xticks([1],[''])
plt.grid()
fig=plt.gcf()
fig.set_size_inches(7,9)	
plt.savefig('voltage_box.png',dpi=100,bbox_inches='tight')
plt.clf()
plt.boxplot(FR)
plt.title('Frequency Boxplot')
plt.ylabel('Frequency (Hz)')
plt.xticks([1],[''])
plt.grid()
fig=plt.gcf()
fig.set_size_inches(7,9)	
plt.savefig('frequency_box.png',dpi=100,bbox_inches='tight')
