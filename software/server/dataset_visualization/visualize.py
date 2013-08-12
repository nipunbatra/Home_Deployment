import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import web
import os
import sys
import time	
import json,datetime,pytz
import numpy as np
from threading import Lock
lock = Lock()
import random

s = json.load(open("bmh_matplotlibrc.json") )
matplotlib.rcParams.update(s)

TIMEZONE='Asia/Kolkata'

urls = ('/query','query',
	'/','home')
	

render = web.template.render('templates')

smart_meter_data=pd.read_csv('/home/nipun/git/Home_Deployment/dataset/smart_meter.csv',index_col=0)['W']
ct_data=pd.read_csv('/home/nipun/git/Home_Deployment/dataset/ct_data_controlled.csv',index_col=0,skipinitialspace=True,names=['id','current'])
light_temp_data=pd.read_csv('/home/nipun/git/Home_Deployment/dataset/light_temp.csv',index_col=0,names=['node','light','temp'])
jplug_data=pd.read_csv('/home/nipun/git/Home_Deployment/dataset/jplug.csv',index_col=0,names=['frequency','voltage','real','energy','cost','current','reactive','apparent','pf','phase','jplug_id'])
pir_data=pd.read_csv('/home/nipun/git/Home_Deployment/dataset/pir.csv',index_col=0,names=['node'])



import random, string

def randomword(length):
	return ''.join(random.choice(string.lowercase) for i in range(length))

class home:
	def GET(self):		
		return render.index()

class query:	
	def POST(self):
		no_data=[]
		plt.clf()
		data = web.data()
		query_data=json.loads(data)
		
		start_time=query_data["start_time"]
		end_time=query_data["end_time"]
		
		ct_id=int(query_data["ct_id"])
		node_id=int(query_data["node_id"])
		jplug_id=query_data["jplug_id"]
		
		idx_smart=(smart_meter_data.index>start_time) & (smart_meter_data.index<end_time)
		smart_meter_power=smart_meter_data[idx_smart]
		x_smart_meter=[datetime.datetime.fromtimestamp(x) for x in smart_meter_data.index[idx_smart]]
		y_smart_meter=smart_meter_power.values
		
		if len(y_smart_meter)==0:
			no_data.append("Smart meter")
		else:
			print len(y_smart_meter),"smart"
		
		ct_required=ct_data[ct_data.id==ct_id].current
		idx_ct=(ct_required.index>start_time) & (ct_required.index<end_time)
		
		ct_current=ct_required[idx_ct]
		x_ct=[datetime.datetime.fromtimestamp(x) for x in ct_current.index]
		y_ct=ct_current.values
		
		if len(y_ct)==0:
			no_data.append("ct")
		else:
			print len(y_ct),"CT"
			
		
		'''Light'''
		idx_light_temp=(light_temp_data.index>start_time) & (light_temp_data.index<end_time)
		df=light_temp_data[idx_light_temp]
		
		y_light=df[df["node"]==node_id].light.values
		idx=y_light>0
		y_light=y_light[idx]
		x_light=[datetime.datetime.fromtimestamp(x) for x in df[df["node"]==node_id][idx].index]
		
		if len(y_light)==0:
			no_data.append("light")
		else:
			print len(y_light),"Light"
		
		'''Temp'''
		y_temp=df[df["node"]==node_id].temp.values
		idx=y_temp>0
		y_temp=y_temp[idx]
		x_temp=[datetime.datetime.fromtimestamp(x) for x in df[df["node"]==node_id][idx].index]
		if len(y_temp)==0:
			no_data.append("temp")
		else:
			print len(y_temp),"Temp"
			
		'''Presence'''
		idx_pir=(pir_data.index>start_time) & (pir_data.index<end_time)
		df_pir=pir_data[idx_pir]
		df_pir=df_pir[df_pir["node"]==node_id]
		y_pir=[1]*len(df_pir.index.values)
		x_pir=[datetime.datetime.fromtimestamp(x) for x in df_pir.index.values]
		if len(x_pir)==0:
			no_data.append("pir")
		
		
		'''jplug'''
		idx_jplug=(jplug_data.index>start_time) & (jplug_data.index<end_time)
		df=jplug_data[idx_jplug]
		
		y_jplug=df[df["jplug_id"]==jplug_id]["real"].values
		x_jplug=[datetime.datetime.fromtimestamp(x) for x in df[df["jplug_id"]==jplug_id].index.values]
		if len(y_jplug)==0:
			no_data.append("jplug")
		else:
			print len(y_jplug),"Jplug"
		
		
		with lock:
			figure = plt.gcf() # get current figure
			num_subplots=6-len(no_data)
			ax1=plt.subplot(num_subplots,1,1)
			#ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
			ax1.set_title('Electricity meter')
			ax1.set_ylabel('Real power (W)')
			if "Smart meter" not in no_data:
				ax1.plot(x_smart_meter,y_smart_meter)
				#plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
			
			count=1
			if "ct" not in no_data:
				count=count+1
				ax2=plt.subplot(num_subplots,1,count,sharex=ax1)
				ax2.set_title("Current for MCB#"+str(ct_id))
				ax2.set_ylabel("Current (A)")
				ax2.plot(x_ct,y_ct)
				#plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
			
			if "light" not in no_data:
				count=count+1
				ax3=plt.subplot(num_subplots,1,count,sharex=ax1)
				ax3.set_title("Light for multisensor# "+str(node_id))
				ax3.set_ylabel("Light intensity %")
				ax3.plot(x_light,y_light)
			if "pir" not in no_data:
				count=count+1
				ax6=plt.subplot(num_subplots,1,count,sharex=ax1)
				ax6.set_title("PIR for multisensor# "+str(node_id))
				ax6.set_ylabel("Motion events")
				ax6.plot(x_pir,y_pir,'o')
			
			if "temp" not in no_data:
				count=count+1
				ax4=plt.subplot(num_subplots,1,count,sharex=ax1)
				ax4.set_title("Temperature for multisensor# "+str(node_id))
				ax4.set_ylabel("Temp (F)")
				ax4.set_ylim((85,100))
				ax4.plot(x_temp,y_temp)
			
			#ax5.set_ylim((85,100))
			if "jplug" not in no_data:
				count=count+1
				ax5=plt.subplot(num_subplots,1,count,sharex=ax1)
				ax5.set_title("Real Power for jplug# "+str(jplug_id))
				ax5.set_ylabel("Real Power (W)")
				ax5.plot(x_jplug,y_jplug)
				
			print no_data
			print "*"*80
			plt.show()
			filename=randomword(12)+".jpg"
			figure = plt.gcf()
			figure.autofmt_xdate()
			figure.set_size_inches(12,num_subplots*2)	
			
			plt.tight_layout()
			plt.savefig("static/images/"+filename, bbox_inches=0,dpi=100)
			plt.close()
			web.header('Content-Type', 'application/json')
			return json.dumps({"filename":filename,"no_data":no_data})
	        
if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()

