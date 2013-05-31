![alt text](https://dl.dropboxusercontent.com/u/75845627/Deployment/Deployment_Home_1.jpg "Deployment in Home I")

This deployment covers the following:

1. Overall electricity meter level data
2. Appliance level data using jPlug and Current Cost Clamp Meter
3. Water meter data
4. CT data
5. Data from Android
6. Alerts- SMS, Email

For each of these you may find more details in the respective Readme files
in corresponding folders.

The following is the port assignment to different services

* 80 - Data from JPlug is written using PhP script to files in /var/www
* 9000- To manually go and check the last 10 readings of individual JPlugs
* 9001- Data from smart meter is upload (CSV's) and can be visualized
* 9002- Data from CT's is uploaded and can be visualized
* 9003- Data from water meter is uploaded (pulses) and can be seen
* 9004- Data from Multisensors is uploaded and can be visualized
* 9009- Memory, CPU, Disk Memory, Client Time
* 9010- An application is run which tells about the status of different deployments done above
