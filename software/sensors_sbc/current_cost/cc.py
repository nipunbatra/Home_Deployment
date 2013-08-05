import serial
import time
import re

ser=serial.Serial("/dev/ttyUSB0",baudrate=57600)
reg_expression_compiled=re.compile(".*<watts>(\d+)<.*")


while True:
        try:
                s=ser.readline()
                f=open('/home/pi/motor_power.csv','a+')
                m=reg_expression_compiled.findall(s)
                string=str(time.time())+","+m[0]+"\n"
                f.write(string)
                f.close()
        except Exception,e:
                continue

