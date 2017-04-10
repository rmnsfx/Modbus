#!/bin/bash

for file in `ls /var/spool/gammu/inbox`
do

    for command in `cat /var/spool/gammu/inbox/$file`
        do
			case "$command" in
            
				'nowuptime')
				priority=A
				echo `uptime` > /var/spool/gammu/outbox/OUT${priority}_+79194622246_00.txt ;;
				  
				'nowdate')
				priority=B
				echo `date` > /var/spool/gammu/outbox/OUT${priority}_+79194622246_00.txt ;;
				
				'reboot')
				echo `sudo reboot` > /var/spool/gammu/outbox/OUT${priority}_+79194622246_00.txt ;;
				
				'status')
				echo `sudo supervisorctl status` > /var/spool/gammu/outbox/OUT${priority}_+79194622246_00.txt ;;
				
				'mem')
				echo `df -h --total | grep total` > /var/spool/gammu/outbox/OUT${priority}_+79194622246_00.txt ;;
							
				esac
				
				
			
        done
done

rm -rf /var/spool/gammu/inbox/*