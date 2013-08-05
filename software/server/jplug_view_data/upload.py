import glob
import os
import time
import requests


DATA_BASE_PATH='/var/www'
URL_PATH="http://11.0.0.100:9005/upload"
THRESHOLD_TIME=900

while True:

    folders=os.listdir(DATA_BASE_PATH)
    try:
        
        for folder in folders:
			print folder
			mypath=str(DATA_BASE_PATH)+str(folder)
			list_of_files= [ f for f in os.listdir(mypath) if os.path.isfile(os.join(mypath,f)) ]
			print list_of_files
			for f in list_of_files:    
				print f
				if int(time.time())-int(os.stat(f).st_mtime)>THRESHOLD_TIME:
					time.sleep(2)
					r=open(f,"r")
					files = {'myfile': r,'folder':folder} 
					g = requests.post(url=URL_PATH,files=files)
					if g.status_code==200:
						os.remove(f)
    except:
        continue
    else:
        pass
    time.sleep(THRESHOLD_TIME)
