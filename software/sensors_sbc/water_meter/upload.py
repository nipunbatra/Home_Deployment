import glob
import os
import time
import requests
THRESHOLD_TIME=900
DATA_BASE_PATH='/home/pi/Desktop/water_data/'
URL_PATH="http://11.0.0.100:9007/upload"
while True:
    try:
        list_of_files=glob.glob(str(DATA_BASE_PATH)+str("/*.csv"))
        print list_of_files
	for f in list_of_files:    
            if int(time.time())-int(os.stat(f).st_mtime)>THRESHOLD_TIME:
                time.sleep(2)
                r=open(f,"r")
		print "Writing "+f
                files = {'myfile': r} 
                g = requests.post(url=URL_PATH,files=files)
		if g.status_code==200:
                    os.remove(f)
    except:
        pass
    time.sleep(THRESHOLD_TIME)
