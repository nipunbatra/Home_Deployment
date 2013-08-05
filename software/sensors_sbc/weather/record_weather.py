#Plotting historical weather data from OPEN Weather API

#Importing the APP ID
from weather_password import APPID

#City ID for Delhi
CITY_ID=1273294
#How much history (Currently could get only 78 records)
COUNT_RECORDS=100
#Base URL
BASE_URL="http://openweathermap.org/data/2.1/history/city/"
#Custom HTTP request URL
REQUEST_URL=BASE_URL+"?id=%d&cnt=%d&APPID=%s" %(CITY_ID,COUNT_RECORDS,APPID)

import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import scipy.stats as st

#Getting historical data
json_data=requests.get(REQUEST_URL).json()
num_records=json_data["cnt"]
print "Response received from server containing %d records" %(num_records)

list_of_records=json_data["list"]

#Pushing humidity, pressure, temperature and timestamp
humidity=[None]*num_records
pressure=[None]*num_records
temperature=[None]*num_records
timestamp=[None]*num_records
dates=[None]*num_records

for i in range(num_records):
	humidity[i]=list_of_records[i]["main"]["humidity"]
	pressure[i]=list_of_records[i]["main"]["pressure"]
	temperature[i]=list_of_records[i]["main"]["temp"]-273.15
	timestamp[i]=list_of_records[i]["dt"]
	dates[i]=datetime.datetime.fromtimestamp(timestamp[i])
	
#Pearson correlation between temperature and pressure
r_correlation=st.pearsonr(pressure,temperature)
print "Correlation b/w temperature and pressure is ",r_correlation

r_correlation=st.pearsonr(humidity,temperature)
print "Correlation b/w temperature and humidity is ",r_correlation
	
#Plotting on 3 subplots and sharing the same x axis to ensure we can equally zoom into all
fig=plt.figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312, sharex=ax1)
ax3 = fig.add_subplot(313, sharex=ax1)

ax1.plot(dates,humidity,'g+-')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H hrs \n%d-%m'))
ax1.set_title('Humidity (%)')

ax2.plot(dates,pressure,'ro-')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H hrs \n%d-%m'))
ax2.set_title('Pressure (hPa)')

ax3.plot(dates,temperature,'b*-')
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H hrs \n%d-%m'))
ax3.set_title('Temperature (Cel)')


plt.tight_layout()
plt.show()



