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
			cursor.execute("DELETE FROM iface_data WHERE datetime <= now()::date - INTERVAL '1 WEEK'")
			returnStr = cursor.statusmessage
			conn.commit()
			conn.close()
			
			write_log('Clean the database OK! (clean_data) \n')
			
			return returnStr
			
def service():		
		
		try:
			conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			
		except:
			write_log('Unable to connect to the database (service) \n')
			conn = None
			conn.close()
			return False
		
		else:		
			cursor = conn.cursor()
			conn.autocommit = True
			cursor.execute("VACUUM iface_data")
			cursor.execute("SELECT pg_size_pretty( pg_database_size( 'client' ) )")
			dbsize = cursor.fetchone()
			
			returnStr = cursor.statusmessage			
			conn.close()
			
			#write_log('Vacuum psql (service) \n')
			write_log('SIZE DB = ' + str("%s" % dbsize) + '\n')
			
			os.system("sudo ./pgcompacttable --user roman --password 1234 --dbname client")
			write_log('Pgcompacttable worked (service) \n')
			
			if int(os.path.getsize('/home/roman/daemon_modbus.log')) > 100000000:
				os.remove('/home/roman/daemon_modbus.log')
				write_log('Remove log file (service) \n')
			
			return returnStr			


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def free_space():
	
	s = os.statvfs('/')
	f = (s.f_bavail * s.f_frsize) / 1048576
	write_log('Free space = ' + str("%s" % f) + ' MB\n')
	
	path = '/home/roman/data/'
	write_log('Data size = ' + str("%s" % int(get_size(path)/1048576) ) + ' MB\n')
	
	# if (f < 1000): 		
		# remove_old()
		# write_log('Remove old files (clean_data) \n')
	
	
def remove_old():

	dir_to_search = '/home/roman/data/'
	for dirpath, dirnames, filenames in os.walk(dir_to_search):
		for file in filenames:
			curpath = os.path.join(dirpath, file)
			file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
			if datetime.datetime.now() - file_modified > datetime.timedelta(days=180):
			  os.remove(curpath)
			  write_log('Remove old files (clean_data) \n')
			
if __name__ == "__main__":	

		# clean_data()
		# service()
		
		
		free_space()
		
		