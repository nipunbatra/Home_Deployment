'''This file will check every 15 mins that connectivity with various systems is maintained and if data from them is coming or not'''
import time,os
import MySQLdb as mdb	
from services import send_mail


#NB: TO add the ID of the 9th and 10th jPlug
JPLUG_ID=["001EC00CC4A0","001EC00CC4A1","001EC00CC4AD","001EC00CC49C","001EC00CC49F","001EC00D7A18","001EC00CC49D","001EC00D7A1D"]
JPLUG_FILE_LOCATION="/var/www/"
JPLUG_THRESHOLD=900

# 1 hour threshold for data
SMART_METER_THRESHOLD=3600

#Connectivity Threshold of 30 mins
CONNECTIVITY_THRESHOLD=1800
#Database where all heartbeat data is maintained
heartbeat_connection = mdb.connect('localhost', 'root', 'password', 'sys_info')
heartbeat_cursor=heartbeat_connection.cursor()

#Database where smart meter data is maintained
smart_meter_data_connection = mdb.connect('localhost', 'root', 'password', 'smart_meter')
smart_meter_data_cursor=smart_meter_data_connection.cursor()

#ID's for checking Heartbeat connections
RPI_SMART_METER_TYPE="RASPBERRY_PI"
RPI_SMART_METER_ID=1



#Finding the difference in last modified time of individual jPlugs
def modification_time(filename):
    return time.time()-os.path.getmtime(filename)
    
def file_exists(filename):
	return os.path.isfile(filename)
	
def jplug_alerts():
	jplug_alert_string=""	
	for jplug in JPLUG_ID:
		if file_exists(JPLUG_FILE_LOCATION+jplug):
			time_since_modification=int(modification_time(JPLUG_FILE_LOCATION+jplug))
			if time_since_modification>JPLUG_THRESHOLD:
				jplug_alert_string=jplug_alert_string+"%s JPlug last sent a packet %d ago.\n"%(jplug,time_since_modification)
		else:
			jplug_alert_string=jplug_alert_string+"%s JPlug has not yet sent a packet.\n"%(jplug)
	return jplug_alert_string
	
def connectivity(client_id,client_type):
	query_string="SELECT server_time FROM sys_info_data where client_id="+str(client_id)+" and client_type= '"+client_type+"' order by server_time desc limit 1"
	heartbeat_cursor.execute(query_string)
	time_seen= heartbeat_cursor.fetchall()[0][0]
	
	time_seen=int(time_seen)
	difference_time=int(time.time())-time_seen
	#print difference_time,"Difference"
	if difference_time> CONNECTIVITY_THRESHOLD:
		return "Client %d of type %s was last seen %d seconds ago"%(client_id,client_type,difference_time)
	else:
		return ""
		
def smart_meter_data():
	query_string="SELECT timestamp from smart_meter_data order by timestamp desc limit 1"
	smart_meter_data_cursor.execute(query_string)
	time_seen=smart_meter_data_cursor.fetchall()[0][0]
	time_seen=int(time_seen)
	difference_time=int(time.time())-time_seen
	#print difference_time
	if difference_time> SMART_METER_THRESHOLD:
		return "Smart Meter data was seen %d seconds ago"%(difference_time)
	else:
		return ""
		
log_file=open('/home/muc/Desktop/Deployment/alerts/sendmail.log','a')	
while True:
	
	#Testing for jPlugs
	overall_alerts=""
	
	#print "Checking for jPlugs"
	overall_alerts+=jplug_alerts()
	#print overall_alerts
	
	#print "Checking for connectivity"
	connectivity_alert_string=connectivity(RPI_SMART_METER_ID,RPI_SMART_METER_TYPE)
	overall_alerts+=connectivity_alert_string
	#print overall_alerts
	
	#print "Checking for data from Smart Meter"
	overall_alerts+=smart_meter_data()
	#print overall_alerts
	try:
		send_mail(overall_alerts)
	except Exception,e:
		log_file.write(str(time.time())+" "+e+"\n")
			#print "-----------------------------------------"
	time.sleep(900)
	
		
    
