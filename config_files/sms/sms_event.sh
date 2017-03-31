#!/bin/bash

# Зададим глобальные переменные.
ADMINPHONE1="79222424223"
ADMINPHONE2="79194622246"
ADMINMAIL=""

# Обработаем только входящие звонки и SMS-сообщения.
# Разделим данные на заголовок и тело сообщения.
if [[ "$1" =~ (CALL|RECEIVED) ]]; then
    MESSAGE=$(cat "$2")
    FROM=$(echo "${MESSAGE}"|grep -e '^From\:'|cut -d' ' -f2)
    DATE=$(echo "${MESSAGE}"|grep -e '^Received\:'|cut -d' ' -f2,3)
    BODY=$(echo "${MESSAGE}"|sed -e '1,/^$/d')
fi

case "$1" in
	# События при входящем звонке.
	CALL)
		# Проверка номера входящего звонка.
		# if [ "${FROM}" == "${ADMINPHONE}" ]; then
			# # Блокировка/разблокировка 22-го порта.
			# # Не забудьте задать следующую строку в файле /etc/sudoers
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

	# События при получении ответа на USSD-запрос.
	USSD)
	;;

	# События при поступлении SMS-сообщения.
	RECEIVED)
	# Проверка номера и тела входящего SMS-сообщения.
		# Если номер совпадает с содержанием переменной ADMINPHONE и тело
		# SMS-сообщения совпадает со словом "REBOOT", то выполняется перезагрузка.
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
			
		else		
			echo -e "Recive sms -> else. From: ${FROM} Date: ${DATE} ${BODY}" 
		fi
	;;
		


	# События при отправке SMS-сообщения.
	# SENT)
	# ;;

	# Прочие события, не определенные выше.
	# *)
		# echo "$*" >>/var/log/sms_recieve_event.log
	# ;;
esac