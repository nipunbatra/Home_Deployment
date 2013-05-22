import psutil,requests,time,json
SERVER_ADDRESS="http://192.168.16.251:9009/upload"
TYPE="RASPBERRY_PI"
ID=1
SLEEP_TIME=900
while True:
	cpu_usage=psutil.cpu_percent()
	mem_free=psutil.avail_phymem()/1000000
	disk_free=psutil.disk_usage('/')[3]
	client_time=int(time.time())
	payload={'cpu_usage':cpu_usage,'mem_free':mem_free,'disk_free':disk_free,'client_time':client_time,'type':TYPE,'client_id':ID}
	headers = {'content-type': 'application/json'}
	r = requests.post(SERVER_ADDRESS, data=json.dumps(payload), headers=headers)
	time.sleep(SLEEP_TIME)

