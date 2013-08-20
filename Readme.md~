## It's different: Insights into home energy consumption in India
##### [Nipun Batra](http://www.nipunbatra.wordpress.com), [Manoj Gulati](http://www.manojgulati.wordpress.com), [Amarjeet Singh](http://www.iiitd.edu.in/~amarjeet/), [Mani Srivastava](http://nesl.ee.ucla.edu/people/mbs/)

###### Special thanks: [Milan Jain](http://milanjain.wordpress.com/), [Shailja Thakur](http://shailjathakur.wordpress.com/)


---

**NB:** You can view a prettier rendering of the same page [here](http://nipunreddevil.github.io/Home_Deployment/).


### Deployment Overview

![alt text](https://dl.dropboxusercontent.com/u/75845627/Deployment/overall_deployment.jpg "Deployment in Home I")

The figure above shows the overall deployment across a 3 storey home in Delhi, India. We deployed a total of 33 sensors measuring the following different parameters:

* Electricity
   * Household level (using Schnieder Electric EM6400 smart meter)
   * MCB level (using custom microcontroller based CT platform)
   * Appliance level (using jPlug, developed by Radio Studio, India)
* Water
   * At inlet from utility and outlet from water tank (using Pulse based water meters)
* Ambient parameters
   * Motion (using Express Controls HSM100)
   * Light, temperature (using Express Controls HSM100 and FunF journal on Android phones)
* Connectivity and Network (using Android, soft sensor streams)
* Weather (using 3 weather monitoring stations providing data via REST APIs)

### Repository Structure

This repository is divided as follows:

* Configuration
   * Database schemas: Schemas for MySQL databases used in the deployment
   * Misc: Miscellaneous mappings between sensor id and locaiton in home
   * Configuration settings: of different sensors. eg. sensitivity of HSM100
   * Inventory: Detailed inventory mentioning all the resources used
* Dataset
   * Annotated dataset: Contains *fully* labeled dataset from our deployment. 
   * Metadata: Contains pertinent metadata for different appliances in the home and different water fixtures
* How To: Misc. how to guides which are not specific to the deployment, but used in our case
* Software:
   * Common: Software common to SBCs and Server
   * Sensors_SBC: Software used by different sensors/SBCs to get data from sensors
   * Server: Software used for server management
   * Startup scripts: Various startup scripts used for uninterrupted data collection (even after power outage)
   * Installation: How to prepare the various computational systems for deployment
   * Stats: Scripts and their outputs used for the plots used in the paper
* Deployment notes

One can also find the various issues and how we resolved them.

1. [Open Issues](https://github.com/nipunreddevil/Home_Deployment/issues?state=open)
2. [Closed Issues](https://github.com/nipunreddevil/Home_Deployment/issues?page=1&state=closed)

### Dataset

1. The detailed metadata dataset can be found [here](https://github.com/nipunreddevil/Home_Deployment/wiki/Appliance-Metadata). This can be visualized [here](http://128.97.93.30:9004/).
2. The UTC timestamped annotated dataset can be found [here](https://github.com/nipunreddevil/Home_Deployment/tree/master/dataset). The event sequence for the same and more information about the same can be found on the same page.

The figure below shows the utlity of multi-modal time synchronized annotations, from one of the days during our deployment.
![alt text](https://dl.dropboxusercontent.com/u/75845627/Deployment/label_annotated.png "Multi-modal annotated data")
