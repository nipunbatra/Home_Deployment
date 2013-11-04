#MySQL server
sudo apt-get install mysql-server

#Python dependencies
sudo apt-get installl python-setuptools
sudo apt-get install python-de
sudo pip install cython
sudo pip install numpy
sudo apt-get install g++
sudo pip install numexpr
sudo pip install pandas
sudo apt-get install python-mysqldb
sudo pip install -U distribute
sudo pip install matplotlib
sudo apt-get install gfortran libopenblas-dev liblapack-dev
sudo pip install scipy

#Now extracting the SQL tar's. Do this for all the SQL DB's downloaded
#Replace your MySQL password, username and DB names
tar -xvzf jplug.sql.tar.gz
mysql -u "username" -p"password"
mysql> create database "dbname;
mysql>exit;
mysql -u "username" -p"yourpassword" "dbname" < /location/"dbname".sql

