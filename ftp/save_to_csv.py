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
			
			df = pd.read_sql_query("SELECT datetime, data, num_reg FROM iface_data WHERE datetime >= now() - interval '6 hour'", conn)						
			df2 = pd.pivot_table(df, index='datetime', columns='num_reg', values='data')
									
			df2.to_csv("/home/roman/data/data.csv", sep=';', header=None, float_format='%.0f')			
			
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
						
		
		print(modbus_data())
				
		
				
