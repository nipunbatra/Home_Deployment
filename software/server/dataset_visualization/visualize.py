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

import pytz

OFFSET=0

TIMEZONE='Asia/Kolkata'

urls = ('/query','query',
	'/','home')
	

render = web.template.render('templates')

smart_meter_data=pd.read_csv('../../../dataset/smart_meter.csv',index_col=0)['W']
ct_data=pd.read_csv('../../../dataset/ct_data_controlled.csv',index_col=0,skipinitialspace=True,names=['id','current'])
light_temp_data=pd.read_csv('../../../dataset/light_temp.csv',index_col=0,names=['node','light','temp'])
jplug_data=pd.read_csv('../../../dataset/jplug.csv',index_col=0,names=['frequency','voltage','real','energy','cost','current','reactive','apparent','pf','phase','jplug_id'])
pir_data=pd.read_csv('../../../dataset/pir.csv',index_col=0,names=['node'])



import random, string

def randomword(length):
	return ''.join(random.choice(string.lowercase) for i in range(length))

class home:
	def GET(self):		
		return render.index()

class query:	
	def POST(self):
		print web.data()
		no_data=[]
		plt.clf()
		data = web.data()
		query_data=json.loads(data)
		
		start_time=query_data["start_time"]
		end_time=query_data["end_time"]
		
		if query_data["ct_id"] is not None:
			ct_ids=[int(x) for x in query_data["ct_id"]]
		else:
			ct_ids=[]
		if query_data["node_id"] is not None:
			node_ids=[int(x) for x in query_data["node_id"]]
		else: node_ids=[]
		if query_data["jplug_id"] is not None:
			jplug_ids=query_data["jplug_id"]
		else:
			jplug_ids=[]
		
		idx_smart=(smart_meter_data.index>start_time) & (smart_meter_data.index<end_time)
		smart_meter_power=smart_meter_data[idx_smart]
		x_smart_meter=[datetime.datetime.fromtimestamp(x-OFFSET) for x in smart_meter_data.index[idx_smart]]
		y_smart_meter=smart_meter_power.values
		
		count=0
		with lock:
			fig = plt.gcf() # get current figure
			ax1=plt.subplot(1,1,1)
			ax1.set_title('Electricity meter')
			ax1.set_ylabel('Real power (W)')
			ax1.plot(x_smart_meter,y_smart_meter)
			count=1
			
		for ct_id in ct_ids:
			ct_required=ct_data[ct_data.id==ct_id].current
			idx_ct=(ct_required.index>start_time) & (ct_required.index<end_time)
			ct_current=ct_required[idx_ct]
			x_ct=[datetime.datetime.fromtimestamp(x-OFFSET) for x in ct_current.index]
			y_ct=ct_current.values
			if len(y_ct)==0:
				no_data.append("ct%d" %ct_id)
			else:
				with lock:
					n = len(fig.axes) 
					for i in range(n): 
						fig.axes[i].change_geometry(n+1, 1, i+1) 
					ax = fig.add_subplot(n+1, 1, n+1,sharex=ax1) 
					ax.set_title('MCB # %d' %ct_id)
					ax.set_ylabel('Current (A)')
					ax.plot(x_ct,y_ct) 
						
		'''Light'''
		for node_id in node_ids:
			idx_light_temp=(light_temp_data.index>start_time) & (light_temp_data.index<end_time)
			df=light_temp_data[idx_light_temp]
			y_light=df[df["node"]==node_id].light.values
			idx=y_light>0
			y_light=y_light[idx]
			x_light=[datetime.datetime.fromtimestamp(x-OFFSET) for x in df[df["node"]==node_id][idx].index]
		
			if len(y_light)==0:
				no_data.append("light%d" %node_id)
			else:
				with lock:
					n = len(fig.axes) 
					for i in range(n): 
						fig.axes[i].change_geometry(n+1, 1, i+1) 
					ax = fig.add_subplot(n+1, 1, n+1,sharex=ax1) 
					ax.plot(x_light,y_light) 
					ax.set_ylabel('Light')
					ax.set_title('Light node #%d' %node_id)
		
		'''Temp'''
		for node_id in node_ids:
			y_temp=df[df["node"]==node_id].temp.values
			idx=y_temp>0
			y_temp=y_temp[idx]
			x_temp=[datetime.datetime.fromtimestamp(x-OFFSET) for x in df[df["node"]==node_id][idx].index]
			if len(y_temp)==0:
				no_data.append("temp%d" %node_id)
			else:
				with lock:
					n = len(fig.axes) 
					for i in range(n): 
						fig.axes[i].change_geometry(n+1, 1, i+1) 
					ax = fig.add_subplot(n+1, 1, n+1,sharex=ax1) 
					ax.plot(x_temp,y_temp) 
					ax.set_ylabel('Temperature (F)')
					ax.set_title('Temperature node #%d' %node_id)
				
			
		'''Presence'''
		for node_id in node_ids:
			idx_pir=(pir_data.index>start_time) & (pir_data.index<end_time)
			df_pir=pir_data[idx_pir]
			df_pir=df_pir[df_pir["node"]==node_id]
			y_pir=[1]*len(df_pir.index.values)
			x_pir=[datetime.datetime.fromtimestamp(x-OFFSET) for x in df_pir.index.values]
			if len(x_pir)==0:
				no_data.append("pir%d" %node_id)
			else:
				with lock:
					n = len(fig.axes) 
					for i in range(n): 
						fig.axes[i].change_geometry(n+1, 1, i+1) 
					ax = fig.add_subplot(n+1, 1, n+1,sharex=ax1) 
					ax.plot(x_pir,y_pir,'o')
					ax.set_ylabel('Presence')
					ax.set_title('PIR node #%d' %node_id) 
				
		
		'''jplug'''
		for jplug_id in jplug_ids:
			idx_jplug=(jplug_data.index>start_time) & (jplug_data.index<end_time)
			df=jplug_data[idx_jplug]
			y_jplug=df[df["jplug_id"]==jplug_id]["real"].values
			x_jplug=[datetime.datetime.fromtimestamp(x-OFFSET) for x in df[df["jplug_id"]==jplug_id].index.values]
			if len(y_jplug)==0:
				no_data.append("jplug %s" %jplug_id)
			else:
				with lock:
					n = len(fig.axes) 
					for i in range(n): 
						fig.axes[i].change_geometry(n+1, 1, i+1) 
					ax = fig.add_subplot(n+1, 1, n+1,sharex=ax1) 
					ax.plot(x_jplug,y_jplug)
					ax.set_title('jPlug Power consumption for %s' %jplug_id)
					ax.set_ylabel('Power (W)')
		
		
		with lock:
			filename=randomword(12)+".jpg"
			figure = plt.gcf()
			figure.autofmt_xdate()
			figure.set_size_inches(6,len(fig.axes)*2)	
			
			plt.tight_layout()
			plt.savefig("static/images/"+filename, bbox_inches=0,dpi=100)
			plt.close()
			web.header('Content-Type', 'application/json')
			return json.dumps({"filename":filename,"no_data":no_data})
	        
if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()

