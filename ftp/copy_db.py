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


def write_log(mes):				
		#f = open('/var/log/daemon_modbus.log', 'w+')
		f = open('/home/roman/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()

def save_to_db():


		try:
		
			conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			cursor = conn.cursor()
			query =	 "INSERT INTO iface_data (data, datetime, num_reg, user_login_id) VALUES (%s, %s, %s, %s);"

		except:			
		
			write_log('Unable to connect to the database \n')
			conn = None
			
		counter = 0
		dev_port = 0
			
		with open('/home/roman/data/new_data.csv', 'rb') as f:
			csv_reader = csv.reader(f, delimiter=';')
		
		# f = open(filename, "w+")
		# f.close()
	
				

if __name__ == "__main__":		
			
		save_to_db()


