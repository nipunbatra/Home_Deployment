import web
import os
import MySQLdb,sys
import time,glob
THRESHOLD_TIME=5
SLEEP_TIME=900
urls = ('/upload', 'Upload')
filedir="/home/muc/Desktop/temp2/"
connection = MySQLdb.Connect(host='', user='root', passwd='password', db='zwave',local_infile = 1)
cursor = connection.cursor()
while True:
	list_of_files=glob.glob(str(filedir)+str("/*.csv"))
	for f in list_of_files: 
		if int(time.time())-int(os.stat(f).st_mtime)>THRESHOLD_TIME:
			try:
				query = "LOAD DATA LOCAL INFILE "+"'"+f+"'"+" INTO TABLE zwave_data FIELDS TERMINATED BY ','  IGNORE 1 LINES"			
				cursor.execute(query)
				connection.commit()
				os.remove(f)
	
			except Exception,e:
				print e
			
	time.sleep(SLEEP_TIME)
 
