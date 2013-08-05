import numpy as np
import datetime
import os
import glob
import MySQLdb
import pytz
import time

connection = MySQLdb.Connect(host='', user='root', passwd='password', db='jplug',local_infile = 1)
cursor = connection.cursor()


JPLUG_ID=["001EC00CC4A0","001EC00CC4A1","001EC00CC4AD","001EC00CC49C","001EC00CC49F","001EC00D7A18","001EC00CC49D","001EC00D7A1D","001EC00D7A1C","001EC00E6BBD","001EC00E6BB6"]

BASE_PATH="/var/www/"



def epoch_to_date(timestamp):
	return datetime.datetime.fromtimestamp(int(timestamp))
	
def epoch_to_date_3(timestamp):
	return datetime.datetime.fromtimestamp(int(timestamp)+19800)
	

def epoch_to_date_2(timestamp):
    return pd.to_datetime(float(timestamp)*int(1e9))

    
def is_timestamp_row(split_line):
    if len(split_line)==1 and len(split_line[0])>2 and "+" not in split_line[0]:
        return True
    else:
        return False
def is_data_row(split_line):
    return len(split_line)>9

def parse_data_row(split_line):
    out=""
    for i in range(10):
        out=out+split_line[i].replace("+","")+","
    return out[:-1]


now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

now_string=str(now.day)+"_"+str(now.month)+"_"+str(now.hour)
print now_string


for jplug in JPLUG_ID:
	print jplug
	list_of_files=os.listdir(BASE_PATH+jplug)
	for f in list_of_files:
		
		if "process" in f or f== now_string:
			if "process" in f:
				if os.path.exists(BASE_PATH+jplug+"/"+f):
					print "Removing"+f
					os.remove(BASE_PATH+jplug+"/"+f)
			
		else:
			print "Reading "+f
			with open(BASE_PATH+jplug+"/"+f) as h:
				
				data=h.readlines()
				print "It has %d lines" %len(data)
				start_found=False
				start_index=0
				while start_found!=True and start_index<len(data): 
					#print data[start_index]
					a=data[start_index].split(" ")
					if is_timestamp_row(a):
						start_found=True
					else:
						start_index+=1
				if start_index==len(data) and start_found!=True:
					print "comt..."
					continue
				timestamp=str(data[start_index])
				print "It has starting timestamp as %s" %timestamp
			print time.sleep(1)
			
			with open(BASE_PATH+jplug+"/"+f+"_processed",'w') as g:
				print "Writing "+f
				g.write("timestamp,frequency,voltage,active_power,energy,cost,current,reactive_power,apparent_power,power_factor,phase_angle,mac\n")
				count=0
				print len(data)
				for i in range(start_index,len(data)):
					line=data[i]
					split_line=line.split(" ")
					if is_timestamp_row(split_line):
						try:
							timestamp=int(split_line[0].replace('\r\n',''))
							count=0
						except: 
							print "pass"
							pass
					elif is_data_row(split_line):
						if len(split_line)>10:
							try:
								if float(split_line[0].replace("+",""))>30.0:
									#Freq should be ~50
									data_row=parse_data_row(split_line)
									g.write(str(timestamp+count)+","+data_row+","+jplug+"\n")
							except:
								continue
						count+=1
					else:
						continue
            
			k=BASE_PATH+jplug+"/"+f+"_processed"
			try:
				query = "LOAD DATA LOCAL INFILE "+"'"+k+"'"+" INTO TABLE jplug_data FIELDS TERMINATED BY ','  IGNORE 1 LINES"
				cursor.execute(query)
				connection.commit()
				if os.path.exists(k):
					os.remove(k)
				if os.path.exists(BASE_PATH+jplug+"/"+f):
					os.remove(BASE_PATH+jplug+"/"+f)
			except Exception,e:
				print e
