import RPi.GPIO as GPIO
import time
import datetime
import pytz

METER_ID="1"
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23, False)
try:
	while True:
		now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

		now_string=METER_ID+"_"+str(now.day)+"_"+str(now.month)+"_"+str(now.hour)
	
		f=open('/home/pi/Desktop/water_data/'+now_string+'.csv','a+')
		
		f.write(METER_ID+","+str(time.time())+","+str(GPIO.input(17))+"\n")
		f.close()
		time.sleep(.2)	
except KeyboardInterrupt:
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup() 	
