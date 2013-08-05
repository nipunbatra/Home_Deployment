import glob
import os
import time
import requests
THRESHOLD_TIME=3600

MOTION_DATA_PATH='/root/multisensor/M_Data/'
URL_PATH='http://11.0.0.100:9004/upload_motion'
try:        
	list_of_files=glob.glob(str(MOTION_DATA_PATH)+str("/*.csv"))		
	for f in list_of_files:    
		if int(time.time())-int(os.stat(f).st_mtime)>THRESHOLD_TIME:				
			r=open(f,"r")
			files = {'myfile': r}      
			g = requests.post(url=URL_PATH,files=files)                
			time.sleep(2)
			if g.status_code==200:
				print "Removing %s"%(f)
				os.remove(f)
				
except :
	a=1
	pass
else:
	a=1
	pass
	
