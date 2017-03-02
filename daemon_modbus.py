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


def mini_modbus():

		try:
			conn = psycopg2.connect("dbname='client' user='postgres2' host='localhost' password='1234'")
		except:
			print('Unable to connect to the database')
			conn = None
			
		#conn = psycopg2.connect("dbname='client' user='postgres2' host='localhost' password='1234'")

		pid = os.getpid()									
		
		while True:
		
				instrument = minimalmodbus.Instrument('/dev/ttyUSB3', 5)				
				#instrument.serial.port			 # this is the serial port name
				instrument.serial.baudrate = 115200	  # Baud
				instrument.serial.bytesize = 8
				#instrument.serial.parity	= serial.PARITY_NONE
				instrument.serial.stopbits = 1
				instrument.serial.timeout  = 0.05	# seconds (50 ms)					
				#instrument.address		# this is the slave address number
				instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode					
				temperature = instrument.read_register(3023-1 , 2, 4, False)	
				
				#print(temperature)
								
				query =	 "INSERT INTO iface_data (data, module_number, user_login_id, datetime, pid) VALUES (%s, %s, %s, %s, %s);"
				data = (temperature, 1, 1, datetime.datetime.now(), pid)
				cursor = conn.cursor()
				cursor.execute(query, data)
				conn.commit()				
				
				
				cursor.execute("SELECT archiving FROM iface_modbussettings WHERE user_login_id = 1")
				state = cursor.fetchall()
				
				if False in state[0]: break							
						#exit(0)				
				
				time.sleep(1)
		
		start_daemon()
						

						
def check_pid(pid):		   
	""" Check For the existence of a unix pid. """
	try:
		os.kill(pid, 0)
	except OSError:
		return False
	else:
		return True				

def start_daemon():

	conn = psycopg2.connect("dbname='client' user='postgres2' host='localhost' password='1234'")
	cursor = conn.cursor()						
	
	while True:										
		
		cursor.execute("SELECT archiving FROM iface_modbussettings WHERE user_login_id = 1")
		state = cursor.fetchall()
		#print(state)
			
		if True in state[0]:								
																			
				mini_modbus()

		time.sleep(1)			

						
if __name__ == "__main__":
						
		if len(sys.argv) == 2:
				if 'start' == sys.argv[1]:
						
						with daemon.DaemonContext():
							start_daemon()						
						
						
				elif 'stop' == sys.argv[1]:
				
						f = open('/home/roman/pid.log', 'r+')
						pid = int(f.readline())				  
						f.close()
						os.kill(pid, signal.SIGTERM)

		# else:
				# print "usage: %s start|stop" % sys.argv[0]
				# sys.exit(2)
				
