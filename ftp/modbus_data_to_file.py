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
		data_list = []		
				
		while True:	
			
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
					if dev_port == 6:
						all_data = template_modbus('/dev/ttyUSB6', 1, 115200, 8, 1, 0.5, 0000, 11, 4)	
					if dev_port == 7:
						all_data = template_modbus('/dev/ttyUSB7', 1, 115200, 8, 1, 0.5, 0000, 11, 4)	
					if dev_port == 8:
						all_data = template_modbus('/dev/ttyUSB8', 1, 115200, 8, 1, 0.5, 0000, 11, 4)	
					if dev_port == 9:
						all_data = template_modbus('/dev/ttyUSB9', 1, 115200, 8, 1, 0.5, 0000, 11, 4)	
						
				except:
					write_log('Unable connect to modbus \n')			
					
					dev_port += 1				
					if dev_port > 9: dev_port = 0					
				
					
				try:
				
					f = open('/home/roman/data/new_data.csv', 'a')
					f.write(str(datetime.datetime.now()))
					f.write(str(';'))	
					for i in all_data:	
						f.write(str(i))				 
						f.write(str(';'))							
					f.write(str('\n'))		
					f.close()
						
				except:				
					write_log('Unable save to file \n')
					
				time.sleep(0.07)


					
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
		
		


