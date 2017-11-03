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
from usb.core import find as finddev
import fcntl
import RPi.GPIO as GPIO





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
		
		port = '/dev/rs485'
		speed = 115200
		buffer_size = 100
		counter = 0		
		except_counter = 0		
		data_list = []		
		Point = namedtuple('Point', ['datetime', 'num_reg', 'value'])
		
		LED = 22
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(LED, GPIO.OUT)
		GPIO.setwarnings(False)
		
		
		while True:											
			
				try:
		
					all_data = template_modbus(port, 1, speed, 8, 1, 0.8, 0000, 11, 4)
					
				except:				
				
					all_data = [0]*11
					
					#write_log('Unable connect to modbus \n')		
					#all_data = None					
                                        
					#if except_counter > 3:
					
						#os.system("sudo usbreset /dev/rs485")
						
						#time.sleep(1)
						
						#os.system("echo '1-1.2' > /sys/bus/usb/drivers/usb/unbind")						
						#os.system("echo '1-1.2' > /sys/bus/usb/drivers/usb/bind")												
						
						#write_log('Reset power 485 (modbus)\n')
						
					if except_counter > 600:		
					
						#write_log('GO REBOOT (modbus)\n')	
						#os.system("sudo reboot")	
						write_log('Unable connect to modbus \n')
						except_counter = 0						
					
					except_counter += 1
															
					#GPIO.cleanup()
				
				finally:
					
					try:
					
						timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:00")
							
						outfilename = '/home/roman/data/{}.csv'.format(timestr)
								
						f = open(outfilename, 'a')
						f.write(str(datetime.datetime.now()))
						f.write(str(';'))		
						for i in all_data:
							f.write(str(i))				 
							f.write(str(';'))							
						f.write(str('\n'))		
						f.close()	
											
					except:				
						write_log('Unable save data to file (modbus)\n')				
	
					else:											
						GPIO.output(LED, True)	
						time.sleep(0.08)											
						GPIO.output(LED, False)
						
						# os.system("sudo echo 1 >/sys/class/leds/led0/brightness")
						# os.system("sudo echo 0 >/sys/class/leds/led0/brightness")
					
					reboot_except_counter = 0
				

				
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
		
		


