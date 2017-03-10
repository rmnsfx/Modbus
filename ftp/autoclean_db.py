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
import ftplib




def write_log(mes):				
		#f = open('/var/log/daemon_modbus.log', 'w+')
		f = open('/home/roman/daemon_modbus.log', 'a')
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		f.write(str(' '))
		f.write(str(mes))				 
		f.close()




def clean_data():
		
		try:
			conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			
		except:
			write_log('Unable to connect to the database (clean_data) \n')
			conn = None
			conn.close()
			return False
		
		else:		
			cursor = conn.cursor()
			cursor.execute("DELETE FROM iface_data WHERE datetime <= now()::date - INTERVAL '1 MONTH'")
			returnStr = cursor.statusmessage
			conn.commit()
			conn.close()
			
			write_log(returnStr)
			
			return returnStr
			
			
if __name__ == "__main__":	

		print( clean_data() )