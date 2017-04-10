#!/bin/bash

# ������� ���������� ����������.
ADMINPHONE1="79222424223"
ADMINPHONE2="79194622246"
ADMINMAIL=""

# ���������� ������ �������� ������ � SMS-���������.
# �������� ������ �� ��������� � ���� ���������.
if [[ "$1" =~ (CALL|RECEIVED) ]]; then
    MESSAGE=$(cat "$2")
    FROM=$(echo "${MESSAGE}"|grep -e '^From\:'|cut -d' ' -f2)
    DATE=$(echo "${MESSAGE}"|grep -e '^Received\:'|cut -d' ' -f2,3)
    BODY=$(echo "${MESSAGE}"|sed -e '1,/^$/d')
fi

case "$1" in
	# ������� ��� �������� ������.
	CALL)
		# �������� ������ ��������� ������.
		# if [ "${FROM}" == "${ADMINPHONE}" ]; then
			# # ����������/������������� 22-�� �����.
			# # �� �������� ������ ��������� ������ � ����� /etc/sudoers
			# #
			# # sms ALL= NOPASSWD: /sbin/iptables
			# #
			# if [ "$(sudo /sbin/iptables -S INPUT|grep -e '--dport 22.*ACCEPT')" ]; then
				# sudo /sbin/iptables -D INPUT -p tcp --dport 22 -j ACCEPT
			# else
				# sudo /sbin/iptables -A INPUT -p tcp --dport 22 -j ACCEPT
			# fi
		# fi
	;;

	# ������� ��� ��������� ������ �� USSD-������.
	USSD)
	;;

	# ������� ��� ����������� SMS-���������.
	RECEIVED)
	# �������� ������ � ���� ��������� SMS-���������.
		# ���� ����� ��������� � ����������� ���������� ADMINPHONE � ����
		# SMS-��������� ��������� �� ������ "REBOOT", �� ����������� ������������.
		if [[ "${FROM}" == "${ADMINPHONE1}" && "$BODY" == "reboot" ]] || [[ "${FROM}" == "${ADMINPHONE2}" && "$BODY" == "reboot" ]]; 
		then
			sudo sendsms 9194622246 "Device reboot"
			sudo reboot
			exit
		
		elif [[ "${FROM}" == "${ADMINPHONE1}" && "$BODY" == "state" ]] || [[ "${FROM}" == "${ADMINPHONE2}" && "$BODY" == "state" ]]; 
		then
			echo -e "From: ${FROM} Date: ${DATE} ${BODY}" 
			OUTPUT="$(sudo supervisorctl status)"					
			sudo sendsms 9194622246 "$OUTPUT"
			exit
		
		elif [[ "${FROM}" == "${ADMINPHONE1}" && "$BODY" == "size" ]] || [[ "${FROM}" == "${ADMINPHONE2}" && "$BODY" == "size" ]]; 
		then
			echo -e "From: ${FROM} Date: ${DATE} ${BODY}" 
			OUTPUT="$(df -h --total | grep total)"					
			sudo sendsms 9194622246 "$OUTPUT"
			exit	
		else		
			echo -e "Recive sms -> else. From: ${FROM} Date: ${DATE} ${BODY}" 
		fi
	;;
		


	# ������� ��� �������� SMS-���������.
	# SENT)
	# ;;

	# ������ �������, �� ������������ ����.
	# *)
		# echo "$*" >>/var/log/sms_recieve_event.log
	# ;;
esac