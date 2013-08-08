### Deployment Overview

![alt text](https://dl.dropboxusercontent.com/u/75845627/Deployment/overall_deployment.jpg "Deployment in Home I")

The figure above shows the overall deployment across a 3 storey home in Delhi, India. We deployed a total of 33 sensors measuring the following different parameters:

1. Electricity
   * Household level (using Schnieder Electric EM6400 smart meter)
   * MCB level (using custom microcontroller based CT platform)
   * Appliance level (using jPlug, developed by Radio Studio, India)
2. Water
   * At inlet from utility and outlet from water tank (using Pulse based water meters)
3. Ambient parameters
   * Motion (using Express Controls HSM100)
   * Light, temperature (using Express Controls HSM100 and FunF journal on Android phones)
4. Connectivity and Network (using Android, soft sensor streams)
5. Weather (using 3 weather monitoring stations providing data via REST APIs)

### Repository Structure

This repository is divided as follows:

* Configuration
   * Database schemas: Schemas for MySQL databases used in the deployment
   * Misc: Miscellaneous mappings between sensor id and locaiton in home
* Dataset
   * Annotated dataset: Contains *fully* labeled dataset from our deployment
   * Metadata: Contains pertinent metadata

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
