import web
import os
import MySQLdb,sys
import time,glob
THRESHOLD_TIME=5
filedir="/home/muc/Desktop/data_dump/motion"
connection = MySQLdb.Connect(host='', user='root', passwd='password', db='multisensor',local_infile = 1)
cursor = connection.cursor()
list_of_files=glob.glob(str(filedir)+str("/*.csv"))
for f in list_of_files: 
	if int(time.time())-int(os.stat(f).st_mtime)>THRESHOLD_TIME:
		try:
			query = "LOAD DATA LOCAL INFILE "+"'"+f+"'"+" INTO TABLE pir FIELDS TERMINATED BY ','  IGNORE 1 LINES"			
				
			cursor.execute(query)
			connection.commit()
				
			os.remove(f)

		except Exception,e:
			print e
			
 

