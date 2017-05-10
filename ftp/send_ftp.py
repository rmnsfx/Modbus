#!/usr/bin/python
# coding: utf-8
from __future__ import generators
import os
import daemon 
import sys
import signal
import time
import logging
from multiprocessing import Process
import minimalmodbus
import psycopg2
import datetime
from datetime import timedelta
import ftplib
import csv
import pandas as pd
import numpy as np
import serial
import threading
from usb.core import find as finddev
from pgdb import connect
import pandas.io.sql as psql
import psycopg2.extensions






def write_log(mes):				
		#f = open('/var/log/daemon_modbus.log', 'w+')
		f = open('/home/roman/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()


def send_ftp(path, name):

	try:
		session = ftplib.FTP('92.53.96.8','npptik_nir','iF0wUAqhD4o0wuBmtH0J')
		file = open(path + name,'rb')
		#os.makedirs(datetime.date.today().strftime("%Y-%m-%d_%h-%m"))
		#result = session.storbinary('STOR /nir/' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.csv', file)		
		result = session.storbinary('STOR /nir/' + name, file)		
		file.close()									
		session.quit()		
		
		write_log('Upload to ftp -> OK\n')	
		
		return True
	
	except:	
		write_log('Unable upload to ftp\n')			
		
		return False
				


				
def modem(state):

		if state == 'start':						
			os.system('sudo /home/roman/modem3g/sakis3g connect APN="internet"')
			
		if state == 'stop':			
			os.system('sudo /home/roman/modem3g/sakis3g disconnect')
								
		if state == 'reset':		
			os.system('sudo /home/roman/modem3g/sakis3g reconnect APN="internet"')
		

def check_ping():
	
	hostname = "8.8.8.8"
	response = os.system("ping -c 1 " + hostname)
	
	# and then check the response...
	if response == 0:
		pingstatus = True
	else:
		pingstatus = False

	return pingstatus
				
				
				
				
				
if __name__ == "__main__":		
			
			restart_counter = 0		
			send_state = False			
				
			while send_state is False:																
					
						modem_ready = False
												
						while modem_ready is False:	
						
							modem('start')									
							write_log('Modem start (ftp)\n')							
							
							if check_ping() is True:								
						
								modem_ready = True
								send_counter = 0
								write_log('Ping ok (ftp)\n')
								
								try:
									#Синхронизируем время
									os.system("sudo ntpdate -bs ntp.remco.org")			
								except:
									write_log('Could not sync the time (ftp)\n')
								
								time.sleep(3)								
								
								while send_state is False:
																			
									timestr = datetime.datetime.now() - datetime.timedelta(hours=1)							
									outfilename = '{}.csv'.format(timestr.strftime("%Y-%m-%d %H:00"))
																												
									if send_ftp('/home/roman/data/', outfilename) is True:
										
										write_log('Data sent, go exit (ftp)\n')											
										modem('stop')								
										send_state = True	
										#os.system('sudo rm /home/roman/data/' + outfilename) #удаляем файлик		
										sys.exit( 0 )			
									
									else:
										
										write_log('Try to send (ftp)\n')											
										modem('reset')										
										#time.sleep(30)
										
										send_counter += 1
										if send_counter > 5:									
											write_log('Exit as can not send to ftp (ftp)\n')
											modem('stop')	
											sys.exit( 0 )										
								
							else:
								write_log('No ping, error init modem (ftp)\n')																							
								modem('reset')
								time.sleep(10)	
								
								restart_counter += 1
								if restart_counter > 5:									
									write_log('Exit as no ping, error init modem (ftp)\n')
									sys.exit( 0 )
									

