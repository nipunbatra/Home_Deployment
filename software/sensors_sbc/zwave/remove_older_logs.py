import os
import time,glob
THRESHOLD_TIME=3600
filedir="/root/multisensor/ZWaveLog/"
list_of_files=glob.glob(str(filedir)+str("/*.csv"))
for f in list_of_files:
	

	if int(time.time())-int(os.stat(f).st_mtime)>THRESHOLD_TIME:
		try:	
			os.remove(f)

		except Exception,e:
			print e
			
 
filedir="/root/multisensor/Log/"
list_of_files=os.listdir(str(filedir))
print list_of_files
for f in list_of_files:
	 if int(time.time())-int(os.stat(filedir+f).st_mtime)>THRESHOLD_TIME:
                try:
                        os.remove(filedir+f)

                except Exception,e:
                        print e

