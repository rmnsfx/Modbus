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
import datetime
import csv
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

def save_modbus():
        
        port = '/dev/rs485'
        speed = 115200
        buffer_size = 200
        counter = 0     
        except_counter = 0      
                        
        LED = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED, GPIO.OUT)
        GPIO.setwarnings(False)
        
        
        
        while True:                                                 
                   
                    
                #Контроллер 
                try:        
                    a1_x = template_modbus(port, 10, 115200, 8, 1, 1, 999, 2, 4, 'float')
                    a2_y = template_modbus(port, 10, 115200, 8, 1, 1, 1001, 2, 4, 'float')
                    a3_z = template_modbus(port, 10, 115200, 8, 1, 1, 1003, 2, 4, 'float')    
                    
                    a4_x = template_modbus(port, 10, 115200, 8, 1, 1, 1005, 2, 4, 'float')
                    a5_y = template_modbus(port, 10, 115200, 8, 1, 1, 1007, 2, 4, 'float')
                    a6_z = template_modbus(port, 10, 115200, 8, 1, 1, 1009, 2, 4, 'float') 
                    
                    a7_x = template_modbus(port, 10, 115200, 8, 1, 1, 1011, 2, 4, 'float')
                    a8_y = template_modbus(port, 10, 115200, 8, 1, 1, 1013, 2, 4, 'float')
                    a9_z = template_modbus(port, 10, 115200, 8, 1, 1, 1015, 2, 4, 'float') 
                    
                    a10_x = template_modbus(port, 10, 115200, 8, 1, 1, 1017, 2, 4, 'float')
                    a11_y = template_modbus(port, 10, 115200, 8, 1, 1, 1019, 2, 4, 'float')
                    a12_z = template_modbus(port, 10, 115200, 8, 1, 1, 1021, 2, 4, 'float') 
                    
                    a13_x = template_modbus(port, 10, 115200, 8, 1, 1, 1023, 2, 4, 'float')
                    a14_y = template_modbus(port, 10, 115200, 8, 1, 1, 1025, 2, 4, 'float')
                    a15_z = template_modbus(port, 10, 115200, 8, 1, 1, 1027, 2, 4, 'float') 
                    
                    a16_x = template_modbus(port, 10, 115200, 8, 1, 1, 1029, 1, 4, 'int')
                    a17_y = template_modbus(port, 10, 115200, 8, 1, 1, 1031, 1, 4, 'int')
                    a18_z = template_modbus(port, 10, 115200, 8, 1, 1, 1033, 1, 4, 'int')                     
                    
                except:                                 
                    a1_x = 0                 
                    a2_y = 0
                    a3_z = 0  
                    a4_x = 0                 
                    a5_y = 0
                    a6_z = 0  
                    a7_x = 0                 
                    a8_y = 0
                    a9_z = 0                      
                    a10_x = 0                 
                    a11_y = 0
                    a12_z = 0  
                    a13_x = 0                 
                    a14_y = 0
                    a15_z = 0  
                    a16_x = 0                 
                    a17_y = 0
                    a18_z = 0                      
                    
                    write_log('Unable get data from PLC\n')  
                    except_counter += 1                 
                
                    
                # print(a1_x, a2_y, a3_z, a4_x, a5_y, a6_z, a7_x, a8_y, a9_z, a10_x, a11_y, a12_z, a13_x, a14_y, a15_z, a16_x, a17_y, a18_z)
                    
                try:
                
                    timestr = roundTime(None, 600).strftime("%d-%m-%Y %H-%M")                   
                    
                    outfilename = '/home/roman/data/{}.csv'.format(timestr)
                            
                    f = open(outfilename, 'a')
                    f.write(str(datetime.datetime.now()))
                    f.write(str(';')) 
                    
                    f.write(str(a1_x).replace('.',','))
                    f.write(str(';'))
                    f.write(str(a2_y).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(a3_z).replace('.',','))
                    f.write(str(';'))

                    f.write(str(a4_x).replace('.',','))
                    f.write(str(';'))
                    f.write(str(a5_y).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(a6_z).replace('.',','))
                    f.write(str(';'))                    
                    
                    f.write(str(a7_x).replace('.',','))
                    f.write(str(';'))
                    f.write(str(a8_y).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(a9_z).replace('.',','))
                    f.write(str(';'))                    

                    f.write(str(a10_x).replace('.',','))
                    f.write(str(';'))
                    f.write(str(a11_y).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(a12_z).replace('.',','))
                    f.write(str(';'))                    
                    
                    f.write(str(a13_x).replace('.',','))
                    f.write(str(';'))
                    f.write(str(a14_y).replace('.',','))                        
                    f.write(str(';'))
                    f.write(str(a15_z).replace('.',','))
                    f.write(str(';'))                    
                    
                    f.write(str(a16_x))
                    f.write(str(';'))
                    f.write(str(a17_y))                        
                    f.write(str(';'))
                    f.write(str(a18_z))
                    f.write(str(';'))                    
					
                    f.write(str('\n'))      
                    f.close()   
                                        
                except:             
                    write_log('Unable save data to file (modbus)\n')          
                    
                        
                time.sleep(0.8)                           

                
def template_modbus(tty, addr, baudrate, bytesize, stopbits, timeout, num_reg, qty, functioncode, type):

        #all_data = []
        
        
        minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = False
        minimalmodbus.precalculate_read_size = False
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
        
        

        
  
        

if __name__ == "__main__":      
            
        save_modbus()
        
        


