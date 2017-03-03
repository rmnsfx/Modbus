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
		f = open('/home/roman/Modbus/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()

def mini_modbus():

		write_log('Start modbus \n')	
		
		try:
			conn = psycopg2.connect("dbname='client' user='postgres2' host='localhost' password='1234'")
		except:
			write_log('Unable to connect to the database (modbus) \n')
			conn = None
			
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
				
				try:				
					query =	 "INSERT INTO iface_data (data, module_number, user_login_id, datetime, pid) VALUES (%s, %s, %s, %s, %s);"
					data = (temperature, 1, 1, datetime.datetime.now(), pid)
					cursor = conn.cursor()
					cursor.execute(query, data)
					conn.commit()				
				except:
					write_log('Unable to save to db (modbus)\n')		
				
				cursor.execute("SELECT archiving FROM iface_modbussettings WHERE user_login_id = 1")
				state = cursor.fetchall()
				
				if False in state[0]: 
					write_log('Stop modbus \n')				
					break		
					
						#exit(0)				
				
				time.sleep(1)
		
		watch_daemon()
						

						
def check_pid(pid):		   
	""" Check For the existence of a unix pid. """
	try:
		os.kill(pid, 0)
	except OSError:
		return False
	else:
		return True				

def watch_daemon():

	write_log('Watch \n')
	
	try:
		conn = psycopg2.connect("dbname='client' user='postgres2' host='localhost' password='1234'")
		cursor = conn.cursor()						
	except:
		write_log('Unable to connect to db (watch state) \n')
	
	while True:										
		
		try:
			cursor.execute("SELECT archiving FROM iface_modbussettings WHERE user_login_id = 1")
			state = cursor.fetchall()
		except:
			write_log('Unable to query data (watch state) \n')
					
		if True in state[0]:																			
				mini_modbus()

		time.sleep(1)			

						
if __name__ == "__main__":
						
		if len(sys.argv) == 2:
				if 'start' == sys.argv[1]:
				
						write_log('First start \n')
						
						with daemon.DaemonContext():
								watch_daemon()						
						
						
				# elif 'stop' == sys.argv[1]:
				
						# f = open('/home/roman/pid.log', 'r+')
						# pid = int(f.readline())				  
						# f.close()
						# os.kill(pid, signal.SIGTERM)

		# else:
				# print "usage: %s start|stop" % sys.argv[0]
				# sys.exit(2)


