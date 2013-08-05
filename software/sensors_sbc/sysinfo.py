import psutil,requests,time,json,subprocess
SERVER_ADDRESS="http://11.0.0.100:9009/upload"
TYPE="Server"
ID=100

while True:
	cpu_usage=psutil.cpu_percent()
	mem_free=psutil.avail_phymem()/1000000
	disk_free=psutil.disk_usage('/')[3]
	proc=subprocess.Popen("ping -c 500 -q google.com",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	packet_loss=100
	avg_ping=0
	return_code=proc.wait()
	stdout_lines=list(proc.stdout)
	for line in stdout_lines:
		if "received" in line and "transimtted" in line:
			split_comma=line.split(",")
		        packet_loss=int(split_comma[2].split("%")[0])
		if "rtt min/avg/max/mdev" in line:
			avg_ping=int(float(line.split("=")[1].split("/")[1]))	
	client_time=int(time.time())
	payload={'cpu_usage':cpu_usage,'mem_free':mem_free,'disk_free':disk_free,'client_time':client_time,'type':TYPE,'client_id':ID,'avg_ping':avg_ping,'packet_loss':packet_loss}
	headers = {'content-type': 'application/json'}
	r = requests.post(SERVER_ADDRESS, data=json.dumps(payload), headers=headers)
	

