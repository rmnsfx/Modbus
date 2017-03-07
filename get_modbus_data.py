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

def write_log(mes):				
		#f = open('/var/log/daemon_modbus.log', 'w+')
		f = open('/home/roman/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()

def save_modbus():

		write_log('Start modbus \n')	
		
		while True:
		
			try:
				conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			except:
				write_log('Unable to connect to the database (modbus) \n')
				conn = None
				
			else:		
						
				r_data1 = template_modbus('/dev/ttyUSB3', 5, 115200, 8, 1, 0.05, 3023-1, 2, 4, False)
				r_data2 = template_modbus('/dev/ttyUSB3', 5, 115200, 8, 1, 0.05, 3023-1, 2, 4, False)
				r_data3 = template_modbus('/dev/ttyUSB3', 5, 115200, 8, 1, 0.05, 3023-1, 2, 4, False)
				r_data4 = template_modbus('/dev/ttyUSB3', 5, 115200, 8, 1, 0.05, 3023-1, 2, 4, False)
				r_data5 = template_modbus('/dev/ttyUSB3', 5, 115200, 8, 1, 0.05, 3023-1, 2, 4, False)
				r_data6 = template_modbus('/dev/ttyUSB3', 5, 115200, 8, 1, 0.05, 3023-1, 2, 4, False)
				r_data7 = template_modbus('/dev/ttyUSB3', 5, 115200, 8, 1, 0.05, 3023-1, 2, 4, False)
				
				#print(str(r_data))	
			
				
				try:				
					query =	 "INSERT INTO iface_data (data, module_number, user_login_id, datetime, num_reg) VALUES (%s, %s, %s, %s, %s);"
					
					data1 = (r_data1, 1, 1, datetime.datetime.now(), 3023)
					data2 = (r_data2, 1, 1, datetime.datetime.now(), 3024)
					data3 = (r_data3, 1, 1, datetime.datetime.now(), 3025)
					data4 = (r_data4, 1, 1, datetime.datetime.now(), 3026)
					data5 = (r_data5, 1, 1, datetime.datetime.now(), 3027)
					data6 = (r_data6, 1, 1, datetime.datetime.now(), 3028)
					data7 = (r_data7, 1, 1, datetime.datetime.now(), 3029)
					
					cursor = conn.cursor()
					
					cursor.execute(query, data1)
					cursor.execute(query, data2)
					cursor.execute(query, data3)
					cursor.execute(query, data4)
					cursor.execute(query, data5)
					cursor.execute(query, data6)
					cursor.execute(query, data7)
					
					conn.commit()				
				
				except:
					write_log('Unable to save to db (modbus)\n')

			
				conn.close()
					
			time.sleep(1)		
			
			
			
				
def template_modbus(tty, addr, baudrate, bytesize, stopbits, timeout, num_reg, value, functioncode, signed):

		instrument = minimalmodbus.Instrument(tty, addr)						
		instrument.serial.baudrate = baudrate	  # Baud
		instrument.serial.bytesize = bytesize
		#instrument.serial.parity	= serial.PARITY_NONE
		instrument.serial.stopbits = stopbits
		instrument.serial.timeout  = timeout	# seconds (50 ms)					
		#instrument.address		# this is the slave address number
		instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode					
		data = instrument.read_register(num_reg, value, functioncode, signed)	
				
		return data
				

if __name__ == "__main__":		
			
		save_modbus()


