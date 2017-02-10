#!/usr/bin/python
# coding: utf-8
import os
import daemon 
import sys
import time
import logging
from multiprocessing import Process
import minimalmodbus


def mini_modbus():
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
				
				print(temperature)
				time.sleep(1)
                        
                        
if __name__ == "__main__":
        #daemon = DaemonClass()
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        #DC = DaemonClass()
                        p = Process(target=mini_modbus)
                        p.start()
                            
                        while True:                                 
                                print("pid = ", p.pid, "state = ", p.is_alive())
                                time.sleep(1)
                        
                                if p.is_alive() == False: 
                                        #DC = DaemonClass()
                                        p = Process(target=mini_modbus)
                                        p.start()
                                
                        
                # elif 'stop' == sys.argv[1]:
                        # #p.terminate()
                # elif 'restart' == sys.argv[1]:
                        # #daemon.restart()
                # else:
                        # print "Unknown command"
                        # sys.exit(2)
                # sys.exit(0)
        # else:
                # print "usage: %s start|stop|restart" % sys.argv[0]
                # sys.exit(2)
                
