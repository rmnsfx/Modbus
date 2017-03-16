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


		
		conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
		cursor = conn.cursor()
		query =	 "INSERT INTO iface_data (data, datetime, num_reg, user_login_id) VALUES (%s, %s, %s, %s);"

			
		
		# write_log('Unable to connect to the database (modbus) \n')
		# conn = None
		
		i=0
		
		while i != 100:			


		
						
			r_data1 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.5, 0000, 0, 4, False)
			# r_data2 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0001, 0, 4, False)
			# r_data3 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0002, 0, 4, False)
			# r_data4 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0003, 0, 4, False)
			# r_data5 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0004, 0, 4, False)
			# r_data6 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0005, 0, 4, False)
			# r_data7 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0006, 0, 4, False)
			# r_data8 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0007, 0, 4, False)
			# r_data9 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0010, 0, 4, False)
			# r_data10 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0011, 0, 4, False)
			# r_data11 = template_modbus('/dev/ttyUSB0', 1, 115200, 8, 1, 0.1, 0012, 0, 4, False)
			
			#print(minimalmodbus._twoByteStringToNum(r_data1, 1, False))
			#print(minimalmodbus._hexencode(r_data1, False))
			print(r_data1)
										
				
							
				
				
			data1 = (r_data1, datetime.datetime.now(), 1, 1)
				# data2 = (r_data2, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 2, 1)
				# data3 = (r_data3, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 3, 1)
				# data4 = (r_data4, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 4, 1)
				# data5 = (r_data5, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 5, 1)
				# data6 = (r_data6, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 6, 1)
				# data7 = (r_data7, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 7, 1)
				# data8 = (r_data8, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 8, 1)
				# data9 = (r_data9, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 9, 1)
				# data10 = (r_data10, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 10, 1)
				# data11 = (r_data11, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 11, 1)
				
				
				
			cursor.execute(query, data1)					
				# cursor.execute(query, data2)					
				# cursor.execute(query, data3)					
				# cursor.execute(query, data4)					
				# cursor.execute(query, data5)					
				# cursor.execute(query, data6)					
				# cursor.execute(query, data7)
				# cursor.execute(query, data8)
				# cursor.execute(query, data9)
				# cursor.execute(query, data10)
				# cursor.execute(query, data11)
				
				#returnStr1 = cursor.statusmessage
				
						
			#except:
				
				#write_log('Unable to save to db (modbus)\n')

			#conn.commit()			
			#cursor.close()
			#conn.close()
			
			i = i+1
			
			time.sleep(0.09)		
			
		
		cursor.close()
		conn.close()
			
			
				
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
		#data = instrument.read_register(num_reg, value, functioncode, signed)	
		#data = instrument.read_register(0000, 0, 4)
		
		
				
		return data
				

if __name__ == "__main__":		
			
		save_modbus()


