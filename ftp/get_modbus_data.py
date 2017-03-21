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
import csv
import pandas as pd
from sqlalchemy import create_engine
import threading
from collections import namedtuple

class Data:
	pass

def write_log(mes):				
		#f = open('/var/log/daemon_modbus.log', 'w+')
		f = open('/home/roman/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()

def save_modbus():


		
		counter = 0
		dev_port = 0
		file_name = '/home/roman/data/data.csv'
		data_list = []
		
		Point = namedtuple('Point', ['datetime', 'num_reg', 'value'])
		
		while counter < 2:	
			
				
		
			# with open(file_name, 'w') as f:
				# writer = csv.writer(f, delimiter = ';')		
			
				# while counter < 100:
			
				try:
					if dev_port == 0:
						all_data = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.5, 0000, 11, 4)			
					if dev_port == 1:
						all_data = template_modbus('/dev/ttyUSB1', 1, 115200, 8, 1, 0.5, 0000, 11, 4)			
					if dev_port == 2:
						all_data = template_modbus('/dev/ttyUSB2', 1, 115200, 8, 1, 0.5, 0000, 11, 4)			
					if dev_port == 3:
						all_data = template_modbus('/dev/ttyUSB3', 1, 115200, 8, 1, 0.5, 0000, 11, 4)			
					if dev_port == 4:
						all_data = template_modbus('/dev/ttyUSB4', 1, 115200, 8, 1, 0.5, 0000, 11, 4)	
					if dev_port == 5:
						all_data = template_modbus('/dev/ttyUSB5', 1, 115200, 8, 1, 0.5, 0000, 11, 4)	
										
				except:
					write_log('Unable connect to modbus\n')			
					
					dev_port += 1				
					if dev_port > 5: dev_port = 0					
				

				#try:
																		
				date = datetime.datetime.now()	
				
				# writer.writerow([date, all_data[0], all_data[1], all_data[2], all_data[3], all_data[4], all_data[5], all_data[6], all_data[7], all_data[8], all_data[9], all_data[10] ])
				
								
				for idx, i in enumerate(all_data):							
					data_list.append(Point(date, idx, i))	
				
				counter += 1
					
					#t = threading.Thread(target=copyto_db)						
					#t.start()
					
				#print(counter)
						
				#except:				
					#write_log('Unable to save to db (modbus)\n')	
					
			
				time.sleep(0.09)
				#f.close()
			
				#if counter >= 10:									
					#counter = 0
					# t = threading.Thread(target=copyto_db)						
					# t.start()
		for g in data_list:
			print(g.datetime, g.num_reg, g.value)
				
def copyto_db():

		#a = None

		#try:			
			
			conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			cursor = conn.cursor()
			engine = create_engine('postgresql://roman:1234@localhost:5432/client')		
			
			#with open('/home/roman/data/new_data.csv') as f:
				#cursor.copy_expert("COPY iface_data(data, datetime, user_login_id, num_reg) FROM STDIN WITH CSV DELIMITER ';'", f)
			
			#conn.commit()
			#cursor.close()
		
		#except:
						
			#write_log('Unable to connect \n')	
		
		#else:	
			
			#df = pd.read_csv('/home/roman/data/new_data.csv', header=None)
			df = pd.read_csv('/home/roman/data/data.csv', sep=';', names = ["datetime", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])				
			
			   
			df = pd.melt(df.reset_index(), id_vars=['datetime'], var_name=['num_reg'], value_name='data')			
			df = df[df.num_reg != 'index'] #убираем строки с появившимся index
			df.to_sql('iface_data', engine, if_exists='append', index=False)
			
			print(df)
		
		#finally:
			
			conn.close()	
		
			
			
		
		
		
		
		
				
def template_modbus(tty, addr, baudrate, bytesize, stopbits, timeout, num_reg, qty, functioncode):

		instrument = minimalmodbus.Instrument(tty, addr)						
		instrument.serial.baudrate = baudrate	  # Baud
		instrument.serial.bytesize = bytesize
		#instrument.serial.parity	= serial.PARITY_NONE
		instrument.serial.stopbits = stopbits
		instrument.serial.timeout  = timeout	# seconds (50 ms)					
		#instrument.address		# this is the slave address number
		instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode			
		all_data = instrument.read_registers(num_reg, qty, functioncode)			
		#data = instrument.read_register(num_reg, value, functioncode, signed)	
		#data = instrument.read_register(0000, 0, 4)		
		
				
		return all_data
				

if __name__ == "__main__":		
			
		save_modbus()
		
		


