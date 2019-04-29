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
        speed = 9600
        buffer_size = 200
        counter = 0     
        except_counter = 0      
                        
        LED = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED, GPIO.OUT)
        GPIO.setwarnings(False)
        
        
        
        while True:                                         
#104                
                try:        
                    a_x = template_modbus(port, 104, 9600, 8, 1, 0.8, 154, 2, 4, 'float')
                    a_y = template_modbus(port, 104, 9600, 8, 1, 0.8, 174, 2, 4, 'float')
                    a_z = template_modbus(port, 104, 9600, 8, 1, 0.8, 194, 2, 4, 'float')                
               
                    v_x = template_modbus(port, 104, 9600, 8, 1, 0.8, 214, 2, 4, 'float')
                    v_y = template_modbus(port, 104, 9600, 8, 1, 0.8, 234, 2, 4, 'float')
                    v_z = template_modbus(port, 104, 9600, 8, 1, 0.8, 254, 2, 4, 'float')               
     
                    x = template_modbus(port, 104, 9600, 8, 1, 0.8, 274, 2, 4, 'int')
                    y = template_modbus(port, 104, 9600, 8, 1, 0.8, 294, 2, 4, 'int')
                    z = template_modbus(port, 104, 9600, 8, 1, 0.8, 314, 2, 4, 'int')            

                except: 
                
                    a_x = 0                 
                    a_y = 0
                    a_z = 0  

                    v_x = 0                 
                    v_y = 0
                    v_z = 0                 
                    
                    x = 0                   
                    y = 0
                    z = 0                           

                    write_log('Unable save data to file (104)\n') 
                    except_counter += 1                 
#110
                try:        
                    a_x2 = template_modbus(port, 110, 9600, 8, 1, 0.8, 154, 2, 4, 'float')
                    a_y2 = template_modbus(port, 110, 9600, 8, 1, 0.8, 174, 2, 4, 'float')
                    a_z2 = template_modbus(port, 110, 9600, 8, 1, 0.8, 194, 2, 4, 'float')                
               
                    v_x2 = template_modbus(port, 110, 9600, 8, 1, 0.8, 214, 2, 4, 'float')
                    v_y2 = template_modbus(port, 110, 9600, 8, 1, 0.8, 234, 2, 4, 'float')
                    v_z2 = template_modbus(port, 110, 9600, 8, 1, 0.8, 254, 2, 4, 'float')               
     
                    x2 = template_modbus(port, 110, 9600, 8, 1, 0.8, 274, 2, 4, 'int')
                    y2 = template_modbus(port, 110, 9600, 8, 1, 0.8, 294, 2, 4, 'int')
                    z2 = template_modbus(port, 110, 9600, 8, 1, 0.8, 314, 2, 4, 'int')            

                except: 
                
                    a_x2 = 0                 
                    a_y2 = 0
                    a_z2 = 0  

                    v_x2 = 0                 
                    v_y2 = 0
                    v_z2 = 0                 
                    
                    x2 = 0                   
                    y2 = 0
                    z2 = 0                           

                    write_log('Unable save data to file (110)\n') 
                    except_counter += 1                 
#112

                try:        
                    a_x3 = template_modbus(port, 112, 9600, 8, 1, 0.8, 154, 2, 4, 'float')
                    a_y3 = template_modbus(port, 112, 9600, 8, 1, 0.8, 174, 2, 4, 'float')
                    a_z3 = template_modbus(port, 112, 9600, 8, 1, 0.8, 194, 2, 4, 'float')                
               
                    v_x3 = template_modbus(port, 112, 9600, 8, 1, 0.8, 214, 2, 4, 'float')
                    v_y3 = template_modbus(port, 112, 9600, 8, 1, 0.8, 234, 2, 4, 'float')
                    v_z3 = template_modbus(port, 112, 9600, 8, 1, 0.8, 254, 2, 4, 'float')               
     
                    x3 = template_modbus(port, 112, 9600, 8, 1, 0.8, 274, 2, 4, 'int')
                    y3 = template_modbus(port, 112, 9600, 8, 1, 0.8, 294, 2, 4, 'int')
                    z3 = template_modbus(port, 112, 9600, 8, 1, 0.8, 314, 2, 4, 'int')            

                except: 
                
                    a_x3 = 0                 
                    a_y3 = 0
                    a_z3 = 0  

                    v_x3 = 0                 
                    v_y3 = 0
                    v_z3 = 0                 
                    
                    x3 = 0                   
                    y3 = 0
                    z3 = 0                           

                    write_log('Unable save data to file (112)\n') 
                    except_counter += 1     
                    
#113

                try:        
                    a_x4 = template_modbus(port, 113, 9600, 8, 1, 0.8, 154, 2, 4, 'float')
                    a_y4 = template_modbus(port, 113, 9600, 8, 1, 0.8, 174, 2, 4, 'float')
                    a_z4 = template_modbus(port, 113, 9600, 8, 1, 0.8, 194, 2, 4, 'float')                
               
                    v_x4 = template_modbus(port, 113, 9600, 8, 1, 0.8, 214, 2, 4, 'float')
                    v_y4 = template_modbus(port, 113, 9600, 8, 1, 0.8, 234, 2, 4, 'float')
                    v_z4 = template_modbus(port, 113, 9600, 8, 1, 0.8, 254, 2, 4, 'float')               
     
                    x4 = template_modbus(port, 113, 9600, 8, 1, 0.8, 274, 2, 4, 'int')
                    y4 = template_modbus(port, 113, 9600, 8, 1, 0.8, 294, 2, 4, 'int')
                    z4 = template_modbus(port, 113, 9600, 8, 1, 0.8, 314, 2, 4, 'int')            

                except: 
                
                    a_x4 = 0                 
                    a_y4 = 0
                    a_z4 = 0  

                    v_x4 = 0                 
                    v_y4 = 0
                    v_z4 = 0                 
                    
                    x4 = 0                   
                    y4 = 0
                    z4 = 0                           

                    write_log('Unable save data to file (113)\n') 
                    except_counter += 1  
                    

                    
                try:
                
                    timestr = datetime.datetime.now().strftime("%d-%m-%Y %H-00")
                        
                    outfilename = '/home/roman/data/{}.csv'.format(timestr)
                            
                    f = open(outfilename, 'a')
                    f.write(str(datetime.datetime.now()))
                    f.write(str(';')) 
#104
                    f.write(str(a_x).replace('.',','))
                    f.write(str(';'))
                    f.write(str(a_y).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(a_z).replace('.',','))
                    f.write(str(';'))
                    
                    f.write(str(v_x).replace('.',','))
                    f.write(str(';'))
                    f.write(str(v_y).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(v_z).replace('.',','))
                    f.write(str(';'))                       
                    
                    f.write(str(x))
                    f.write(str(';'))
                    f.write(str(y))                        
                    f.write(str(';'))
                    f.write(str(z))
                    f.write(str(';')) 

#110
                    f.write(str(a_x2).replace('.',','))
                    f.write(str(';'))
                    f.write(str(a_y2).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(a_z2).replace('.',','))
                    f.write(str(';'))
                    
                    f.write(str(v_x2).replace('.',','))
                    f.write(str(';'))
                    f.write(str(v_y2).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(v_z2).replace('.',','))
                    f.write(str(';'))                       
                    
                    f.write(str(x2))
                    f.write(str(';'))
                    f.write(str(y2))                        
                    f.write(str(';'))
                    f.write(str(z2))
                    f.write(str(';'))                     

#112

                    f.write(str(a_x3).replace('.',','))
                    f.write(str(';'))
                    f.write(str(a_y3).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(a_z3).replace('.',','))
                    f.write(str(';'))
                    
                    f.write(str(v_x3).replace('.',','))
                    f.write(str(';'))
                    f.write(str(v_y3).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(v_z3).replace('.',','))
                    f.write(str(';'))                       
                    
                    f.write(str(x3))
                    f.write(str(';'))
                    f.write(str(y3))                        
                    f.write(str(';'))
                    f.write(str(z3))
                    f.write(str(';')) 
					
#113

                    f.write(str(a_x4).replace('.',','))
                    f.write(str(';'))
                    f.write(str(a_y4).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(a_z4).replace('.',','))
                    f.write(str(';'))
                    
                    f.write(str(v_x4).replace('.',','))
                    f.write(str(';'))
                    f.write(str(v_y4).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(v_z4).replace('.',','))
                    f.write(str(';'))                       
                    
                    f.write(str(x4))
                    f.write(str(';'))
                    f.write(str(y4))                        
                    f.write(str(';'))
                    f.write(str(z4))
                    f.write(str(';')) 					

                    
                    f.write(str('\n'))      
                    f.close()   
                                        
                except:             
                    write_log('Unable save data to file (modbus)\n')          
                    
                        
                time.sleep(1)                           

                
def template_modbus(tty, addr, baudrate, bytesize, stopbits, timeout, num_reg, qty, functioncode, type):

        #all_data = []
        
        
        #minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
        instrument = minimalmodbus.Instrument(tty, addr)                        
        instrument.serial.baudrate = baudrate     # Baud
        instrument.serial.bytesize = bytesize
        #instrument.serial.parity   = serial.PARITY_NONE
        instrument.serial.stopbits = stopbits
        instrument.serial.timeout  = timeout    # seconds (50 ms)                   
        #instrument.address     # this is the slave address number
        instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode          
        #all_data = instrument.read_registers(num_reg, qty, functioncode)            
        #all_data = instrument.read_register(num_reg, 0, functioncode, signed=True)            
        #instrument.debug=True
        
        if type == 'float':
            all_data = instrument.read_float(num_reg, functioncode, 2)                         
        if type == 'int':
            all_data = instrument.read_register(num_reg, 0, functioncode, signed=True)            
            
        #data = instrument.read_register(num_reg, value, functioncode, signed)  
        #data = instrument.read_register(0000, 0, 4)        
                        
        return all_data

        
# def get_size(start_path):
    # total_size = 0
    # for dirpath, dirnames, filenames in os.walk(start_path):
        # for f in filenames:
            # fp = os.path.join(dirpath, f)
            # total_size += os.path.getsize(fp)
    # return total_size     

# def free_space():
    
    # s = os.statvfs('/')
    # f = (s.f_bavail * s.f_frsize) / 1048576
    # write_log('Free space = ' + str("%s" % f) + ' MB\n')
    
    # path = '/home/roman/data/'
    # write_log('Data size = ' + str("%s" % int(get_size(path)/1048576) ) + ' MB\n')
    
    # if (f < 1000):        
        # remove_old()
        # write_log('Remove old files \n')

        
# def remove_old():

    # dir_to_search = '/home/roman/data/'
    # for dirpath, dirnames, filenames in os.walk(dir_to_search):
        # for file in filenames:
            # curpath = os.path.join(dirpath, file)
            # file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
            # if datetime.datetime.now() - file_modified > datetime.timedelta(days=180):
              # os.remove(curpath)
              # write_log('Remove old files (clean_data) \n')       
        

if __name__ == "__main__":      
            
        save_modbus()
        
        


