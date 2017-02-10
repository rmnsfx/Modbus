#!/usr/bin/python
# coding: utf-8

import sys
import os
import minimalmodbus
import daemon 
from multiprocessing import Process, Pipe
import time

def mini_modbus(baudrate, bytesize, stopbits, timeout):
        #f = open('/tmp/data.log', 'w')
        #f.write(str(temperature))                
        #f.close()
        while True:
                
                instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 5)
                
                #instrument.serial.port          # this is the serial port name
                instrument.serial.baudrate = baudrate   # Baud
                instrument.serial.bytesize = bytesize
                #instrument.serial.parity   = serial.PARITY_NONE
                instrument.serial.stopbits = stopbits
                instrument.serial.timeout  = timeout   # seconds (50 ms)
                    
                #instrument.address     # this is the slave address number
                instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode  
                
                temperature = instrument.read_register(3023-1 , 2, 4, False)    
                                
                #print(temperature)

                time.sleep(1)
                
                

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'): 
        
        
        # Выполнить первое ветвление процесса, 
        try: 
        
            pid = os.fork() 
            
            if pid > 0:                 
                sys.exit(0) # Первый родительский процесс завершает работу, 
                    
            
        except OSError, e: 
            sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror)) 
            sys.exit(1) 
        
        #Отключиться от родительского окружения. 
        os.chdir("/") 
        os.umask(0) 
        os.setsid() 
        
        # Выполнить второе ветвление, 
        try: 
            pid2 = os.fork() 
            
            #if pid2 > 0: 
                #sys.exit(0)  #Второй родительский процесс завершает работу, 
            
        except OSError, e: 
            sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror)) 
            sys.exit(1) 
            
        # Теперь процесс стал демоном, выполнить перенаправление стандартных дескрипторов 
        
        if pid2 != 0:   
        
                for f in sys.stdout, sys.stderr: f.flush() 
                si = file(stdin, 'r') 
                so = file(stdout, "a+") 
                se = file(stderr, "a+", 0) 
                os.dup2(si.fileno(), sys.stdin.fileno()) 
                os.dup2(so.fileno(), sys.stdout.fileno()) 
                os.dup2(se.fileno(), sys.stderr.fileno()) 
        
        if pid2 == 0:   
        while True:                     
                print(check_pid(pid2))
                time.sleep(2) 
       

                
        
        
def check_pid(pid):        
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

        
        
if __name__ == "__main__":

        daemonize(stdout='/home/roman/data.log', stderr='/home/roman/err.log')
        mini_modbus(115200, 8, 1, 1)
        

