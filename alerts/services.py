import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
from password import gmail_username,gmail_password
gmail_user =gmail_username
gmail_pwd = gmail_password

def mail(to, subject, text):
   msg = MIMEMultipart()
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
   msg.attach(MIMEText(text)) 
   print msg 
   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   b=mailServer.ehlo()
   print b
   c=mailServer.starttls()
   print c
   d=mailServer.ehlo()
   print d
   e=mailServer.login(gmail_user, gmail_pwd)
   print e
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()


def send_mail(information):
	mail("nipunb@iiitd.ac.in","Sensor Data Warnings",information)
	
