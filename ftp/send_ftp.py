#!/usr/bin/python
# coding: utf-8
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
import ftplib
import csv
import pandas as pd
import numpy as np
import serial
import threading
from usb.core import find as finddev

last_datetime = None

def write_log(mes):				
		#f = open('/var/log/daemon_modbus.log', 'w+')
		f = open('/home/roman/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()

def modbus_data():			
				
		#result = None
		
		try:
		
			conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			cursor = conn.cursor()
			#df = pd.read_sql_query("SELECT datetime, data, num_reg FROM iface_data WHERE datetime >= DATE_TRUNC('hour', now()::date) - interval '1 hour'", conn)					
			#df = pd.read_sql_query("SELECT datetime, data, num_reg FROM iface_data WHERE datetime BETWEEN '2017-03-27 19:00' AND '2017-03-27 23:00'", conn)					
			df = pd.read_sql_query("SELECT datetime, data, num_reg FROM iface_data WHERE datetime BETWEEN (date_trunc('hour', now()::timestamp) - INTERVAL '1 HOUR') AND date_trunc('hour', now()::timestamp)", conn)					
			
			
			df2 = pd.pivot_table(df, index='datetime', columns='num_reg', values='data')									
			df2.to_csv("/home/roman/data/data.csv", sep=';', header=None, float_format='%.0f')						
			conn.close()
			
			return True
			
		except:
			
			write_log('Unable to connect to the database (modbus_data) \n')			
			conn = None
			conn.close()
			
			return False
		
		
			
			# cursor.execute("SELECT concat(data, ' ', datetime) FROM iface_data WHERE (datetime >= now()::date - INTERVAL '12 HOUR')", [num_reg])			
						
			# #os.makedirs(datetime.date.today().strftime("%Y/%m/%d"))
			# f = open('/home/roman/data/%s' % num_reg, 'w')
			# for row in cursor:
				# print>>f, row[0]		

			#cursor.execute("SELECT datetime, data, num_reg FROM iface_data WHERE (datetime >= now()::date - INTERVAL '12 HOUR')")					
			#result = cursor.fetchall()
			#f = open("/home/roman/data/data.csv","wb")
			#c = csv.writer(f)
			#c.writerows(result)			
			#f.close()
			

			
			
		

def send_ftp(path, name):

	try:
		session = ftplib.FTP('92.53.96.8','npptik_nir','iF0wUAqhD4o0wuBmtH0J')
		file = open(path + name,'rb')
		#os.makedirs(datetime.date.today().strftime("%Y-%m-%d_%h-%m"))
		result = session.storbinary('STOR /nir/data_' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.csv', file)		
		file.close()									
		session.quit()		
		
		write_log('Upload to ftp -> OK\n')	
		
		return True
	
	except:	
		write_log('Unable upload to ftp\n')			
		
		return False
				
def send_log():
		
		try:
		
			session = ftplib.FTP('92.53.96.8','npptik_nir','iF0wUAqhD4o0wuBmtH0J')
			
			file1 = open('/var/log/supervisor/supervisord.log','r')
			# file2 = open('/var/log/modbus_error.log','r')
			# file3 = open('/var/log/wvdial_error.log','r')
			# file4 = open('/var/log/send_ftp_error.log','r')
			# file5 = open('/home/roman/daemon_modbus.log','r')
			session.storbinary('STOR /nir/log/', file1)		
			# session.storbinary('STOR /nir/log' , file2)		
			# session.storbinary('STOR /nir/log/', file3)		
			# session.storbinary('STOR /nir/log/', file4)				
			# session.storbinary('STOR /nir/log/', file5)
			file1.close()				
			# file2.close()
			# file3.close()
			# file4.close()
			# file5.close()
			
			session.quit()	
			
		except:
		
			write_log('Unable upload log to ftp\n')			

def modem(state):

		if state == 'start':			
			# os.system('sudo wvdial &')
			os.system('sudo /home/roman/modem3g/sakis3g connect APN="internet"')

			
		if state == 'stop':
			# os.system("sudo killall -9 wvdial &")
			# os.system("sudo killall -9 pppd &")
			os.system('sudo /home/roman/modem3g/sakis3g disconnect')
			
		# if state == 'reboot':
			# mod=serial.Serial("/dev/ttyUSB0",115200,timeout=5)
			# mod.write("AT+CFUN=1,1\r")
			# mod.close()	
			
		# if state == 'AT':
			# mod=serial.Serial("/dev/megafon-modem",9600,timeout=5)
			# mod.write("AT+CFUN=1")
			# mod.close()		
			
		if state == 'reset':
			dev = finddev(idVendor=0x12d1)
			dev.reset()	
		

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
						
				
			while True:
									
				
					if modbus_data() is True:				
											
						send_state = False						
						modem_ready = False
						
						while modem_ready is False:	
						
							modem('start')		
							#time.sleep(5)
							write_log('Modem start (ftp)\n')							
							
							if check_ping() is True:								
						
								modem_ready = True
								send_counter = 0
								write_log('Ping ok (ftp)\n')
								
								while send_state is False:
																								
									if send_ftp('/home/roman/data/', 'data.csv') is True:
										
										write_log('Data sent, go sleep (ftp)\n')											
										modem('stop')								
										os.system('sudo /etc/init.d/sms3 restart') #перезагружаем смс		
										#time.sleep(60 * 60 * 1) #1 час						
										send_state = True	
										sys.exit( 0 )			
									
									else:
										write_log('Try to send (ftp)\n')	
										time.sleep(5)			
								
							else:
								write_log('No ping, error init modem (ftp)\n')	
								modem('stop')																	
								modem('reset')
								time.sleep(5)	
								
					else:
						write_log('Error fetch data from db (ftp)\n')						
						time.sleep(5)				
						
					os.system("sudo sh -c 'echo 3 >/proc/sys/vm/drop_caches'" )
