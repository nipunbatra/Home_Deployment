import web,json,datetime,pytz,time

TIMEZONE='Asia/Kolkata'

urls = ("/upload","upload")
app = web.application(urls, globals())
db = web.database(dbn='mysql', db='sys_info', user='root', pw='password')

class upload:
	
	def POST(self):
		data = web.data()
		query_data=json.loads(data)
		cpu_usage=int(query_data["cpu_usage"])
		mem_free=query_data["mem_free"]
		disk_free=int(query_data["disk_free"])
		client_time=query_data["client_time"]
		client_type=query_data["type"]
		client_id=query_data["client_id"]
		server_time=int(time.time())
		avg_ping=query_data["avg_ping"]
		packet_loss=query_data["packet_loss"]
		db.insert('sys_info_data',cpu_usage=cpu_usage,mem_free=mem_free,disk_free=disk_free,client_time=client_time,client_type=client_type,client_id=client_id,server_time=server_time,avg_ping=avg_ping,packet_loss=packet_loss)
		return "alpha"
		

if __name__ == "__main__":
    app.run()
