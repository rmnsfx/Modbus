#!/usr/bin/python
# coding: utf-8
from __future__ import generators
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
from datetime import timedelta
import ftplib
import csv
import pandas as pd
import numpy as np
import serial
import threading
from usb.core import find as finddev
from pgdb import connect
import pandas.io.sql as psql
import psycopg2.extensions






def write_log(mes):             
        #f = open('/var/log/daemon_modbus.log', 'w+')
        f = open('/home/roman/daemon_modbus.log', 'a')
        f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        f.write(str(' '))
        f.write(str(mes))                
        f.close()


def send_ftp(path, name):

    #try:
    session = ftplib.FTP('92.53.96.8','npptik_nir','iF0wUAqhD4o0wuBmtH0J')
    file = open(path + name,'rb')
        #os.makedirs(datetime.date.today().strftime("%Y-%m-%d_%h-%m"))
        #result = session.storbinary('STOR /nir/' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.csv', file)       
    result = session.storbinary('STOR /nir/01/' + name, file)       
    file.close()                                    
    session.quit()      
        
    write_log('Upload to ftp -> OK\n')  
        
    return result
    
    #except: 
        #write_log('Unable upload to ftp\n')         
        
        #return False
                


                
def modem(state):

        if state == 'start':                        
            os.system('sudo /home/roman/modem3g/sakis3g connect APN="internet"')
            
        if state == 'stop':         
            os.system('sudo /home/roman/modem3g/sakis3g disconnect')
                                
        if state == 'reset':        
            phone = serial.Serial("/dev/megafon-modem",  baudrate=9600, timeout=5) 
            phone.write("AT+CFUN=1\r\n")
            phone.close()
        
            os.system('sudo /home/roman/modem3g/sakis3g reconnect APN="internet" >> /home/roman/daemon_modbus.log')
        

def check_ping():
    
    hostname = "8.8.8.8"
    response = os.system("ping -c 1 " + hostname)
    
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False

    return pingstatus
                
def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo

   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)                  

   
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
    
    path = '/home/roman/'
    write_log('Data size = ' + str("%s" % int(get_size(path)/1048576) ) + ' MB\n')
    
    # if (f < 1000):        
        # remove_old()
        # write_log('Remove old files \n')                
                
if __name__ == "__main__":      
            
            restart_counter = 0     
            send_state = False
                        
                
            while send_state is False:                                                              
                    
                        modem_ready = False
                                                
                        while modem_ready is False: 
                        
                            modem('start')                                  
                            write_log('Modem start (ftp)\n')                            
                            
                            if check_ping() is True:                                
                        
                                modem_ready = True
                                send_counter = 0
                                write_log('Ping ok (ftp)\n')
                                
                                try:
                                    #Синхронизируем время
                                    os.system("sudo ntpdate -bs ntp.remco.org")         
                                except:
                                    write_log('Could not sync the time (ftp)\n')
                                
                                #time.sleep(3)                               
                                
                                while send_state is False:
                                                                            
                                    #timestr = datetime.datetime.now() - datetime.timedelta(minutes=10)                                                             
                                    #outfilename = '{}.csv'.format(timestr.strftime("%d-%m-%Y %H-%M"))
                                            
                                    timestr = roundTime(None, 600).strftime("%d-%m-%Y %H-%M") #10 min                                       
                                    outfilename = '/home/roman/data/{}.csv'.format(timestr)                                         
                                            
                                    for root, dirs, files in os.walk('/home/roman/data/'):
                                        files.sort()                                    
                                        for filename in files:
                                            
                                            print('filename: ' + filename)         
                                            print('outfilename: ' + outfilename)
                                            
                                            if filename in outfilename:                                                  
                                                modem('stop')                               
                                                send_state = True
                                                free_space()                                                
                                                sys.exit( 0 )                                           
                                                                                                            
                                            if send_ftp('/home/roman/data/', filename) is True:
                                            
                                                write_log('Data sent to ftp ' + filename + '\n')                                         
                                                #print('sent')
                                                #modem('stop')                               
                                                #send_state = True   
                                                #os.system('sudo rm /home/roman/data/' + outfilename) #delete       
                                                os.rename('/home/roman/data/' + filename, '/home/roman/sent/' + filename) #remove to 'sent' dir

                                                
                                                #sys.exit( 0 )           
                                            
                                            else:
                                                
                                                write_log('Try to send (ftp)\n')                                            
                                                print('try send again')
                                                
                                                #modem('reset')                                      
                                                time.sleep(1)
                                                
                                                send_counter += 1
                                                if send_counter > 5:                                    
                                                    write_log('Exit as can not send to ftp (ftp)\n')
                                                    modem('stop')   
                                                    sys.exit( 0 )                                       
                                                 
                                
                            else:
                                write_log('No ping or error init modem (ftp)\n')                                                                                          
                                modem('reset')
                                time.sleep(60)  
                                
                                restart_counter += 1
                                if restart_counter > 6:                                 
                                    write_log('Exit as no ping, error init modem (ftp)\n')
                                    sys.exit( 0 )
                                    

