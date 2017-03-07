#!/bin/bash

while :; do 

	flock -n /tmp/lock_modbus -c "python /home/roman/get_modbus_data.py" &
	sleep 5; 
done