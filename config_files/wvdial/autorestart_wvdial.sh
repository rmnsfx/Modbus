#!/bin/bash

#while :; do
#  wvdial &
#  sleep 5
#done

while :; do 

	flock -n /tmp/lock_wvdial -c wvdial & 
	sleep 5; 
done