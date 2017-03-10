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

last_datetime = None

def write_log(mes):				
		#f = open('/var/log/daemon_modbus.log', 'w+')
		f = open('/home/roman/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()

def modbus_data():
			
				
		result = None
		
		try:
			conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			
		except:
			write_log('Unable to connect to the database (read_modbus_data) \n')
			conn = None
			conn.close()
			return False
		
		else:		
			cursor = conn.cursor()
			# cursor.execute("SELECT concat(data, ' ', datetime) FROM iface_data WHERE (datetime >= now()::date - INTERVAL '12 HOUR')", [num_reg])			
						
			# #os.makedirs(datetime.date.today().strftime("%Y/%m/%d"))
			# f = open('/home/roman/data/%s' % num_reg, 'w')
			# for row in cursor:
				# print>>f, row[0]		

			cursor.execute("SELECT * FROM iface_data WHERE (datetime >= now()::date - INTERVAL '12 HOUR')")
			result = cursor.fetchall()
			
			f = open("/home/roman/data/data.csv","wb")
			c = csv.writer(f)
			c.writerows(result)			
			f.close()
			conn.close()
			
			return True
		

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
				
				
if __name__ == "__main__":		
			
		#time.sleep(3600)
		
		
		while True:			
			
			if modbus_data() is True:				
			
				send_state = False				
				
				while send_state is False:
					
					if send_ftp('/home/roman/data/', 'data.csv') is True:			
						#time.sleep(600)
						time.sleep(3600) #12 часов
						send_state = True		
					
					else:
				
						time.sleep(60)
						
					
					
				
			else:
				
				time.sleep(5)
				
		
				
