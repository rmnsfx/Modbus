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
		
		buffer_size = 100
		counter = 0
		dev_port = 0		
		data_list = []		
		Point = namedtuple('Point', ['datetime', 'num_reg', 'value'])
		
		while True:	
			
				try:
					if dev_port == 0:
						all_data = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.8, 0000, 11, 4)			
					if dev_port == 1:
						all_data = template_modbus('/dev/ttyUSB1', 1, 115200, 8, 1, 0.8, 0000, 11, 4)			
					if dev_port == 2:
						all_data = template_modbus('/dev/ttyUSB2', 1, 115200, 8, 1, 0.8, 0000, 11, 4)			
					if dev_port == 3:
						all_data = template_modbus('/dev/ttyUSB3', 1, 115200, 8, 1, 0.8, 0000, 11, 4)			
					if dev_port == 4:
						all_data = template_modbus('/dev/ttyUSB4', 1, 115200, 8, 1, 0.8, 0000, 11, 4)	
					if dev_port == 5:
						all_data = template_modbus('/dev/ttyUSB5', 1, 115200, 8, 1, 0.8, 0000, 11, 4)	
					if dev_port == 6:
						all_data = template_modbus('/dev/ttyUSB6', 1, 115200, 8, 1, 0.8, 0000, 11, 4)	
					if dev_port == 7:
						all_data = template_modbus('/dev/ttyUSB7', 1, 115200, 8, 1, 0.8, 0000, 11, 4)	
					if dev_port == 8:
						all_data = template_modbus('/dev/ttyUSB8', 1, 115200, 8, 1, 0.8, 0000, 11, 4)	
					if dev_port == 9:
						all_data = template_modbus('/dev/ttyUSB9', 1, 115200, 8, 1, 0.8, 0000, 11, 4)	
						
				except:
					write_log('Unable connect to modbus \n')			
					write_log(str( 'current usb port# ' + str(dev_port)+ '\n' ))
					
					
					dev_port += 1				
					if dev_port > 9: dev_port = 0					
				

				try:																		
					date = datetime.datetime.now()	
								
					for idx, i in enumerate(all_data):							
						data_list.append(Point(date, idx, i))	
						
				except:				
					write_log('Unable append namedtuple to list (modbus)\n')
					
				
				
				
				if counter >= buffer_size:						
				
					#start_time = time.time()
				
					counter = 0				
					threads = [] 
					fork = True
					
					try: pid = os.fork()
					
					except:
						write_log( "Ошибка создания дочернего процесса" )
						fork = False
						
					else:
						if pid == 0 : # дочерний процесс
							copyto_db(data_list)
							
							sys.exit( 0 )
							
						if pid > 0 :  # родительский процесс
							#os.wait()							
							signal.signal(signal.SIGCHLD,signal.SIG_IGN) # игнорируем зомби 
							
					
					#Реинициализация списка
					data_list = None
					data_list = []
				
					#end_time = time.time()					
					#print (end_time - start_time)	
				
				else:
					time.sleep(0.09)
				
				
				counter += 1
					
				
def copyto_db(data):

		labels = ['datetime', 'num_reg', 'data']

		try:
			engine = create_engine('postgresql://roman:1234@localhost:5432/client')					
			
			df = pd.DataFrame.from_records(data, columns=labels)
			df.to_sql('iface_data', engine, if_exists='append', index=False)
		
		except:						
			write_log('Unable save to db \n')	
		
			sys.exit( 0 )
		
		#else:				
			#df = pd.read_csv('/home/roman/data/new_data.csv', header=None)
			#df = pd.read_csv('/home/roman/data/data.csv', sep=';', names = ["datetime", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])						   
			#df = pd.melt(df.reset_index(), id_vars=['datetime'], var_name=['num_reg'], value_name='data')			
			#df = df[df.num_reg != 'index'] #убираем строки с появившимся index
			
			#conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			#cursor = conn.cursor()
			
			#with open('/home/roman/data/new_data.csv') as f:
				#cursor.copy_expert("COPY iface_data(data, datetime, user_login_id, num_reg) FROM STDIN WITH CSV DELIMITER ';'", f)
			
			#conn.commit()
			#cursor.close()			
		
		#finally:			
			# conn.close()				
			
		# for i in data:
			# print(i.datetime, i.num_reg, i.value)
		
		
		
		
				
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
		
		


