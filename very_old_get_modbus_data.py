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
        data_list = []      
        #Point = namedtuple('Point', ['datetime', 'num_reg', 'value'])
        
        LED = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED, GPIO.OUT)
        GPIO.setwarnings(False)
        
        
        
        while True:                                         
            
                try:
        
                    data1 = template_modbus(port, 61, 9600, 8, 1, 0.8, 0001, 1, 4)
                    data1[0] = data1[0] * 0.01
                    
                except:             
                
                    data1 = [0]*1                   
                    except_counter += 1
                
                finally:
                    
                    try:
                    
                        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:00")
                            
                        outfilename = '/home/roman/data/61_{}.csv'.format(timestr)
                                
                        f = open(outfilename, 'a')
                        f.write(str(datetime.datetime.now()))
                        f.write(str(';'))       
                        for i in data1:
                            f.write(str(i))              
                            f.write(str(';'))                           
                        f.write(str('\n'))      
                        f.close()   
                                            
                    except:             
                        write_log('Unable save data to file (modbus 61)\n')             
    

                    
                
                
                
                try:
        
                    data2 = template_modbus(port, 65, 9600, 8, 1, 0.8, 0001, 1, 4)
                    data2[0] = data2[0] * 0.01
                    
                except:             
                
                    data2 = [0]*1                   
                    except_counter += 1                 

                finally:
                    
                    try:
                    
                        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:00")
                            
                        outfilename = '/home/roman/data/65_{}.csv'.format(timestr)
                                
                        f = open(outfilename, 'a')
                        f.write(str(datetime.datetime.now()))
                        f.write(str(';'))       
                        for i in data2:
                            f.write(str(i))              
                            f.write(str(';'))                           
                        f.write(str('\n'))      
                        f.close()   
                                            
                    except:             
                        write_log('Unable save data to file (modbus 65)\n')     




                try:
        
                    data3 = template_modbus(port, 67, 9600, 8, 1, 0.8, 0001, 1, 4)
                    data3[0] = data3[0] * 0.01
                    
                except:             
                
                    data3 = [0]*1                   
                    except_counter += 1                 

                finally:
                    
                    try:
                    
                        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:00")
                            
                        outfilename = '/home/roman/data/67_{}.csv'.format(timestr)
                                
                        f = open(outfilename, 'a')
                        f.write(str(datetime.datetime.now()))
                        f.write(str(';'))       
                        for i in data3:
                            f.write(str(i))              
                            f.write(str(';'))                           
                        f.write(str('\n'))      
                        f.close()   
                                            
                    except:             
                        write_log('Unable save data to file (modbus 67)\n')     
                        
                        
                        
                        
#Контроллер 481                
                
                try:
        
                    data_4 = template_modbus(port, 10, 9600, 8, 1, 0.8, 154, 100, 4)
                                        
                except:             
                
                    data_4 = [0]*1                                        
                    except_counter += 1                 

                finally:
                    
                    try:
                    
                        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:00")
                            
                        outfilename = '/home/roman/data/10_1_{}.csv'.format(timestr)
                                
                        f = open(outfilename, 'a')
                        f.write(str(datetime.datetime.now()))
                        f.write(str(';'))       
                        for i in data_4:
                            f.write(str(i))              
                            f.write(str(';'))                           
                        f.write(str('\n'))      
                        f.close()   
                                            
                    except:             
                        write_log('Unable save data to file (modbus 10)\n')          

                        
                        
                        
                        
                try:
                
                    data_5 = template_modbus(port, 10, 9600, 8, 1, 0.8, 254, 70, 4)
                    
                except:                             
                              
                    data_5 = [0]*1
                    except_counter += 1                 

                finally:
                    
                    try:
                    
                        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:00")
                            
                        outfilename = '/home/roman/data/10_2_{}.csv'.format(timestr)
                                
                        f = open(outfilename, 'a')
                        f.write(str(datetime.datetime.now()))
                        f.write(str(';'))       
                        for i in data_5:
                            f.write(str(i))              
                            f.write(str(';'))                           
                        f.write(str('\n'))      
                        f.close()   
                                            
                    except:             
                        write_log('Unable save data to file (modbus 10)\n')                         
                

                        
                        
                time.sleep(1)                           

                
def template_modbus(tty, addr, baudrate, bytesize, stopbits, timeout, num_reg, qty, functioncode):

        all_data = []
        
        #minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
        instrument = minimalmodbus.Instrument(tty, addr)                        
        instrument.serial.baudrate = baudrate     # Baud
        instrument.serial.bytesize = bytesize
        #instrument.serial.parity   = serial.PARITY_NONE
        instrument.serial.stopbits = stopbits
        instrument.serial.timeout  = timeout    # seconds (50 ms)                   
        #instrument.address     # this is the slave address number
        instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode          
        all_data = instrument.read_registers(num_reg, qty, functioncode)            
        #all_data = instrument.read_register(num_reg, 0, functioncode, signed=True)            
        #all_data = instrument.read_float(num_reg, functioncode, 2)                         
        #data = instrument.read_register(num_reg, value, functioncode, signed)  
        #data = instrument.read_register(0000, 0, 4)        
        
                
        return all_data
                

if __name__ == "__main__":      
            
        save_modbus()
        
        


