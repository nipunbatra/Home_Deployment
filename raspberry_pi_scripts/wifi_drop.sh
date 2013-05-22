#!/bin/bash
######################################################
#Script used to check that Wi-Fi is working or not####
while true ; do
	if ifconfig wlan0 | grep -q "inet addr:" ; then
		sleep 60
	else
		echo "Network conn down! Attempting Reconn"
		ifdown --force wlan0
		sleep 10		
		ifup --force wlan0
		sleep 10
	fi
done

