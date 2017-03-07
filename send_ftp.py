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

last_datetime = None

def write_log(mes):				
		#f = open('/var/log/daemon_modbus.log', 'w+')
		f = open('/home/roman/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()

def modbus_data(num_reg):
		
		# write_log('Start modbus \n')	
		
		#num_reg = 3023
		
		try:
			conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			
		except:
			write_log('Unable to connect to the database (read_modbus_data) \n')
			conn = None
		
		else:		
			cursor = conn.cursor()
			cursor.execute("SELECT concat(data, ' ', datetime) FROM iface_data WHERE num_reg = %s", [num_reg])
			#data1 = cursor.fetchall()			

			#os.makedirs(datetime.date.today().strftime("%Y/%m/%d"))
			f = open('/home/roman/data/%s' % num_reg, 'w')
			for row in cursor:
				print>>f, row[0]
			
			f.close()
		
		finally:	
			conn.close()
		
		return True

def send_ftp(path, name):

	#try:
	session = ftplib.FTP('92.53.96.8','npptik_nir','iF0wUAqhD4o0wuBmtH0J')
	file = open(path + name,'rb')				   # file to send
	#os.makedirs(datetime.date.today().strftime("%Y-%m-%d_%h-%m"))
	session.storbinary('STOR /nir/' + name + ' ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file)		# send the file
	file.close()									# close file and FTP
	session.quit()
	
	# except:	
		# write_log('Unable to upload to ftp\n')		
		# return False
				

if __name__ == "__main__":		
			
		#time.sleep(3600)
		
		while True:			
			
			if modbus_data(3023) is True:				
			
				send_state = False
				
				while send_state is False:
					
					if send_ftp('/home/roman/data/', '3023') is True:			
						time.sleep(60)
						#time.sleep(3600) 12 часов
						last_datetime = datetime.datetime.now()
					
					else:
						time.sleep(10)			
			else:
				time.sleep(10)
				
		
				
