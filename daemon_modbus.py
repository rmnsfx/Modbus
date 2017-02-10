#!/usr/bin/python
# coding: utf-8
import os
import daemon 
import sys
import time
import logging
from multiprocessing import Process, Pipe
import minimalmodbus
from new1 import daemonize

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
                                
                print(temperature)
                                
                time.sleep(1)
                
                
    
if __name__ == "__main__":

        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        
                        #DC = DaemonClass()                        
                        #p = Process(target=DC.mini_modbus, args=())
                        #p.start()                        
                        #daemonize(stdout='/tmp/data.log',stderr='/tmp/err.log')
                        daemonize()
                        pid = mini_modbus(115200, 8, 1, 0.05)
                        #while True:
                                #print(str(p.pid))
                                #if p.is_alive() == False:
                                        #p.start()                        
                                #time.sleep(1)

                elif 'stop' == sys.argv[1]:
                        p.terminate()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
                
