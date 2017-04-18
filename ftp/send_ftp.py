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

last_datetime = None

def ResultIter(cursor, arraysize=1000):
	'An iterator that uses fetchmany to keep memory usage down'
	while True:
		results = cursor.fetchmany(arraysize)
		if not results:
			break
		for result in results:
			yield result


def write_log(mes):				
		#f = open('/var/log/daemon_modbus.log', 'w+')
		f = open('/home/roman/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()

def modbus_data():			
				
		#result = None
		
		#try:
	
			#-------------
			#PSYCOPG2
			#-------------
			conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			#conn.autocommit = True
									
			cursor = conn.cursor(name='things')
			cursor1 = conn.cursor(name='test')
			
			cursor.itersize = 10000
			
			#cursor.execute(" SELECT datetime, data, num_reg FROM iface_data WHERE datetime BETWEEN (date_trunc('hour', now()) - INTERVAL '1 HOUR') AND date_trunc('hour', now()) ")
			
			cursor.execute(" SELECT datetime, data, num_reg FROM iface_data WHERE datetime >= (date_trunc('hour', now()) - INTERVAL '1 HOUR') AND datetime < date_trunc('hour', now()) ")
			
			cursor1.execute("SELECT COUNT(*) FROM iface_data WHERE datetime >= (date_trunc('hour', now()) - INTERVAL '1 HOUR') AND datetime < date_trunc('hour', now())")
			
			row_count = cursor1.fetchone()
			row = int(row_count[0])
									
			#print(row)
			write_log(row)
			
			get_flag = False
			
			while not get_flag:
					
				i = 0
				
				while True:
					#try:
										
						chunk = cursor.fetchmany(10000)
						if not chunk:
							break;
						
						i +=len(chunk)
						
						print(i)
						
						df2 = pd.DataFrame( chunk ) #Конвертируем list в pandas dataframe				
						df2.columns = ['datetime', 'data', 'num_reg']	 #Добавляем заголовки		
						df3 = pd.pivot_table(df2, index='datetime', columns='num_reg', values='data') #Преобразуем таблицу	
						df3.to_csv("/home/roman/data/data.csv", sep=';', header=None, float_format='%.0f', mode ='a')	
					
					#except psycopg2.Error, e:
						
						#print(e)
		
				if row == i:
				
					#print("GOOD!")
					write_log("Fetch all data (modbus_data)")
					
					get_flag = True			
					conn.close()			
					return True	
				
				else:
					
					write_log("Fetch not all try once again (modbus_data)")
					os.system('sudo rm /home/roman/data/data.csv') #удаляем файлик							
					
					print(row, i)
			
			

			# all_row = []			
			# while True:			
				# row = cursor.fetchone()						
				# if row == []:
					# break;				
				# all_row.append(row)				
			# print(all_row)	
				
			#chunk = cursor.fetchall() #Получаем list	

		# except psycopg2.OperationalError as e:
			# print(e)
			# write_log(str('psycopg2 error: %s \n', e))			

			# if conn:			
				# conn.close()
			
			
			
			#-------------			
			#PANDAS	
			#-------------
			#df = pd.read_sql_query("SELECT datetime, data, num_reg FROM iface_data WHERE datetime BETWEEN (date_trunc('hour', now()::timestamp) - INTERVAL '1 HOUR') AND date_trunc('hour', now()::timestamp)", conn)	
			
			#chunk
			#for chunk in pd.read_sql_query("SELECT datetime, data, num_reg FROM iface_data WHERE datetime BETWEEN (date_trunc('hour', now()::timestamp) - INTERVAL '1 HOUR') AND date_trunc('hour', now()::timestamp)", conn, chunksize=100000):
				#print(chunk)
			
			#df2 = pd.pivot_table(df2, index='datetime', columns='num_reg', values='data')									
			#df2.to_csv("/home/roman/data/data.csv", sep=';', header=None, float_format='%.0f')		
			
			#-------------			
			#PyGreSQL
			#-------------
			#conn = connect(dbname='client', user='roman', host='localhost', password='1234')
			#cursor = conn.cursor()			
			#cursor.execute("SELECT datetime, data, num_reg FROM iface_data WHERE datetime BETWEEN (date_trunc('hour', now()::timestamp) - INTERVAL '1 HOUR') AND date_trunc('hour', now()::timestamp)")			
			#df = cursor.fetchall()		
			#-------------
								

			
		#except:
			
			#write_log('Unable to connect to the database (modbus_data) \n')			
			#conn = None
			
			#return False
		

			
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
			
			#df = pd.read_sql_query("SELECT datetime, data, num_reg FROM iface_data WHERE datetime >= DATE_TRUNC('hour', now()::date) - interval '1 hour'", conn)					
			#df = pd.read_sql_query("SELECT datetime, data, num_reg FROM iface_data WHERE datetime BETWEEN '2017-03-27 19:00' AND '2017-03-27 23:00'", conn)					
			#cursor.itersize = 10000 # how much records to buffer on a client
			#df = cursor.fetchall() #Получаем list	
			

			
			
		

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
			
			restart_counter = 0		
			send_state = False			
				
			while send_state is False:									
				
					if modbus_data() is True:				
					
						modem_ready = False
												
						while modem_ready is False:	
						
							modem('start')		
							#time.sleep(5)
							write_log('Modem start (ftp)\n')							
							
							if check_ping() is True:								
						
								modem_ready = True
								send_counter = 0
								write_log('Ping ok (ftp)\n')
								
								#Синхронизируем время
								os.system("sudo ntpdate -bs ntp.remco.org")			
								time.sleep(3)								
								
								while send_state is False:
																								
									if send_ftp('/home/roman/data/', 'data.csv') is True:
										
										write_log('Data sent, go exit (ftp)\n')											
										modem('stop')								
										#os.system('sudo /etc/init.d/sms3 restart') #перезагружаем смс		
										#time.sleep(60 * 60 * 1) #1 час						
										send_state = True	
										os.system('sudo rm /home/roman/data/data.csv') #удаляем файлик		
										sys.exit( 0 )			
									
									else:
										write_log('Try to send (ftp)\n')	
										modem('stop')	
										modem('reset')
										modem('start')	
										time.sleep(5)			
								
							else:
								write_log('No ping, error init modem (ftp)\n')	
								modem('stop')																	
								modem('reset')
								time.sleep(60)	
								
								restart_counter += 1
								if restart_counter > 5:									
									write_log('Exit as no ping, error init modem (ftp)\n')
									sys.exit( 0 )
									
								
					else:
						write_log('Error fetch data from db (ftp)\n')						
						time.sleep(5)				
						
					#os.system("sudo sh -c 'echo 3 >/proc/sys/vm/drop_caches'" )
