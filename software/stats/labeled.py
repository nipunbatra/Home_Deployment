'''This script finds the total number of entries in a day for smart meter'''


import pandas as pd
import MySQLdb
import pandas.io.sql as psql
mysql_conn_smart_meter=MySQLdb.connect(user='root',passwd='password',db='smart_meter')
mysql_conn_water_meter=MySQLdb.connect(user='root',passwd='password',db='water')
mysql_conn_jplug=MySQLdb.connect(user='root',passwd='password',db='jplug')
mysql_conn_multisensor=MySQLdb.connect(user='root',passwd='password',db='multisensor')


import matplotlib

import datetime
import time
import pytz
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size': 22})


start_timestamp=1373550000
end_timestamp=start_timestamp+2*60*60

'''Smart meter'''
query='select timestamp,W from smart_meter_data where timestamp between %d and %d;' %(start_timestamp,end_timestamp)
result=psql.frame_query(query,mysql_conn_smart_meter)
y_smart=result['W'].values
x_smart=[datetime.datetime.fromtimestamp(x) for x in result['timestamp'].values]

ax1=plt.subplot(5,2,1)
ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
ax1.set_title('Electricity meter')
ax1.set_ylabel('Real power (W)')
ax1.plot(x_smart,y_smart)
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))



'''PIR Ground floor'''
query='select timestamp from pir where node_id=7 and timestamp between %d and %d;' %(start_timestamp,end_timestamp)
result=psql.frame_query(query,mysql_conn_multisensor)

y_pir_6=[1]*len(result['timestamp'].values)
x_pir_6=[datetime.datetime.fromtimestamp(x) for x in result['timestamp'].values]
ax2=plt.subplot(5,2,3,sharex=ax1)
ax2.plot(x_pir_6,y_pir_6,'go')
ax2.set_title("PIR ground floor")
ax2.set_ylabel("Motion events")
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))


'''Light Ground floor'''
query='select timestamp,light from light_temp where node_id=7 and timestamp between %d and %d;' %(start_timestamp,end_timestamp)
result=psql.frame_query(query,mysql_conn_multisensor)

y_light_6=result['light'].values
idx=y_light_6>30
y_light_6=y_light_6[idx]
x_light_6=[datetime.datetime.fromtimestamp(x) for x in result['timestamp'].values[idx]]
ax3=plt.subplot(5,2,5,sharex=ax1)
ax3.set_title("Light ground floor")
ax3.set_ylabel("Light intensity %")
ax3.plot(x_light_6,y_light_6)

'''PIR First floor'''
query='select timestamp from pir where node_id=4 and timestamp between %d and %d;' %(start_timestamp,end_timestamp)
result=psql.frame_query(query,mysql_conn_multisensor)

y_pir_4=[1]*len(result['timestamp'].values)
x_pir_4=[datetime.datetime.fromtimestamp(x) for x in result['timestamp'].values]
ax4=plt.subplot(5,2,7,sharex=ax1)
ax4.set_title("PIR first floor")
ax4.set_ylabel("Motion events")
ax4.plot(x_pir_4,y_pir_4,'go')

'''Light First floor'''
query='select timestamp,light from light_temp where node_id=4 and timestamp between %d and %d;' %(start_timestamp,end_timestamp)
result=psql.frame_query(query,mysql_conn_multisensor)

y_light_4=result['light'].values
idx=y_light_4>25	
y=y_light_4[idx]
x_=result['timestamp'].values[idx]
x_light_4=[datetime.datetime.fromtimestamp(x) for x in x_]
ax5=plt.subplot(5,2,4,sharex=ax1)
ax5.set_title("Light first floor")
ax5.set_ylabel("Light intensity %")
ax5.plot(x_light_4,y)


'''jplug first floor laptop'''
query="SELECT active_power,timestamp FROM jplug_data WHERE mac='001EC00D7A18' and timestamp BETWEEN %d and %d;" %(start_timestamp,end_timestamp)
result=psql.frame_query(query,mysql_conn_jplug)

y_jplug=result['active_power'].values
x_jplug=[datetime.datetime.fromtimestamp(x) for x in result['timestamp'].values]
ax6=plt.subplot(5,2,6,sharex=ax1)
ax6.set_ylabel("Real Power(W)")
ax6.set_title("Laptop jPlug")
ax6.plot(x_jplug,y_jplug)

'''jplug first floor AC'''
query="SELECT active_power,timestamp FROM jplug_data WHERE mac='001EC00CC49F' and timestamp BETWEEN %d and %d;" %(start_timestamp,end_timestamp)
result=psql.frame_query(query,mysql_conn_jplug)

y_jplug_ac=result['active_power'].values
x_jplug_ac=[datetime.datetime.fromtimestamp(x) for x in result['timestamp'].values]
ax7=plt.subplot(5,2,8,sharex=ax1)
ax7.set_ylabel("Real Power(W)")
ax7.set_title("Air conditioner jPlug")
ax7.plot(x_jplug_ac,y_jplug_ac)

'''Temp First floor'''
query='select timestamp,temp from light_temp where node_id=4 and timestamp between %d and %d;' %(start_timestamp,end_timestamp)
result=psql.frame_query(query,mysql_conn_multisensor)

y_light_4=result['temp'].values
idx=y_light_4>25	
y=y_light_4[idx]
x_=result['timestamp'].values[idx]
x_light_4=[datetime.datetime.fromtimestamp(x) for x in x_]
ax8=plt.subplot(5,2,10,sharex=ax1)
ax8.set_title("Temperature first floor")
ax8.set_ylabel("Temperature (F)")
ax8.plot(x_light_4,y)

#plt.tight_layout()
fig = plt.gcf()
#fig.autofmt_xdate()
fig.set_size_inches(15,30)	
plt.savefig('label.png',dpi=100,bbox_inches='tight')

plt.tight_layout()
plt.show()

'''
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
'''

