import glob
import os
import time
import MySQLdb
import pytz
import time
THRESHOLD_TIME=10
connection = MySQLdb.Connect(user='root', passwd='password', db='water',local_infile = 1)
cursor = connection.cursor()

DATA_BASE_PATH='/home/muc/Desktop/water_data/'
try:
    list_of_files=glob.glob(str(DATA_BASE_PATH)+str("/*.csv"))
    print list_of_files
    for f in list_of_files:
        if int(time.time())-int(os.stat(f).st_mtime)>THRESHOLD_TIME:
            time.sleep(2)
	    query= "LOAD DATA LOCAL INFILE "+"'"+ f+  "' INTO TABLE water_data FIELDS TERMINATED BY ','  IGNORE 1 LINES"
	    cursor.execute(query)
	    connection.commit()
	    os.remove(f)

except Exception,e:
    print e
    pass
    
