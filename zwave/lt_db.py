import web
import os
import MySQLdb,sys
import time,glob
THRESHOLD_TIME=5
filedir="/home/muc/Desktop/data_dump/lt"
connection = MySQLdb.Connect(host='', user='root', passwd='password', db='multisensor',local_infile = 1)
cursor = connection.cursor()
list_of_files=glob.glob(str(filedir)+str("/*.csv"))
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler(filedir+'/lt_db.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
for f in list_of_files: 
	if int(time.time())-int(os.stat(f).st_mtime)>THRESHOLD_TIME:
		try:
			query = "LOAD DATA LOCAL INFILE "+"'"+f+"'"+" INTO TABLE light_temp FIELDS TERMINATED BY ','  IGNORE 1 LINES"			
				
			cursor.execute(query)
			connection.commit()
			logger.info("Removing "+f)
			os.remove(f)

		except Exception,e:
			logger.error('Failed to write CSV to file', exc_info=True)
			
 

