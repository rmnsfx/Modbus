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



def mini_modbus():

        pid = os.getpid()                            
        f = open('/home/roman/pid.log', 'w')
        f.write(str(pid))                
        f.close()
        
        while True:
        
                instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 5)                
                #instrument.serial.port          # this is the serial port name
                instrument.serial.baudrate = 115200   # Baud
                instrument.serial.bytesize = 8
                #instrument.serial.parity   = serial.PARITY_NONE
                instrument.serial.stopbits = 1
                instrument.serial.timeout  = 0.05   # seconds (50 ms)                   
                #instrument.address     # this is the slave address number
                instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode                  
                temperature = instrument.read_register(3023-1 , 2, 4, False)    
                
                #print(temperature)
                time.sleep(1)
                        
                        
if __name__ == "__main__":
        		        
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:        

                        with daemon.DaemonContext():                            
                            mini_modbus()
                            
                        # while True:                                 
                                # print("pid = ", p.pid, "state = ", p.is_alive())
                                # time.sleep(1)
                        
                                # if p.is_alive() == False:         
                                        # p = Process(target=mini_modbus)
                                        # p.start()
                        
                elif 'stop' == sys.argv[1]:
				
                        f = open('/home/roman/pid.log', 'r+')
                        pid = int(f.readline())               
                        f.close()
                        os.kill(pid, signal.SIGTERM)

        # else:
                # print "usage: %s start|stop" % sys.argv[0]
                # sys.exit(2)
                
