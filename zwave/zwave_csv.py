import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import web
import os
import MySQLdb,sys
import time	
import json,datetime,pytz
import numpy as np
from threading import Lock
lock = Lock()
import random
units={}
units["lighting"]="Percentage"
units["temperature"]="Celsius"


TIMEZONE='Asia/Kolkata'

urls = ('/upload', 'Upload',
		'/query','query',
		'/','home')
filedir="/home/muc/Desktop/temp2/"
render = web.template.render('templates')
db = web.database(dbn='mysql', db='zwave', user='root', pw='password')

import random, string

def randomword(length):
	return ''.join(random.choice(string.lowercase) for i in range(length))

class home:
	def GET(self):
		
		return render.index()

class Upload:
   def POST(self):
	
        x = web.input(myfile={})
        
        
        if 'myfile' in x: # to check if the file-object is created
			filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			path=filedir		
			
			if not os.path.exists(path):
				os.makedirs(path)
			fout = open(path+ filename,'w') # creates the file where the uploaded file should be stored
			fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
			fout.close() # closes the file, upload complete.
			
			
class query:
	
	def POST(self):
		data = web.data()
		query_data=json.loads(data)
		start_time=query_data["start_time"]
		end_time=query_data["end_time"]
		
		parameter=query_data["parameter"]
		query="SELECT "+parameter+",timestamp FROM zwave_data WHERE timestamp BETWEEN "+str(start_time)+" AND "+str(end_time)
		
		retrieved_data=list(db.query(query))
		
		LEN=len(retrieved_data)
		x=[0]*LEN
		y=[0]*LEN
		X=[None]*LEN
		for i in range(0,LEN):
			x[i]=retrieved_data[i]["timestamp"]
			y[i]=retrieved_data[i][parameter]
			
			X[i]=datetime.datetime.fromtimestamp(x[i],pytz.timezone(TIMEZONE))
			
		#print retrieved_data["timestamp"]
		with lock:
			figure = plt.gcf() # get current figure
			plt.axes().relim()
			plt.title(parameter+" vs Time")
			plt.xlabel("Time")
			plt.ylabel(units[parameter])
			plt.axes().autoscale_view(True,True,True)
			figure.autofmt_xdate()
			plt.plot(X,y)
			filename=randomword(12)+".jpg"
			plt.savefig("/home/muc/Desktop/Deployment/zwave/static/images/"+filename, bbox_inches=0,dpi=100)
			plt.close()
			
			web.header('Content-Type', 'application/json')
			return json.dumps({"filename":filename})
			
		
		

        
if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()

