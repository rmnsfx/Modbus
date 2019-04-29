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
import csv
import pandas as pd
import numpy as np
import serial
import threading
from usb.core import find as finddev

if __name__ == "__main__":	

			conn = psycopg2.connect("dbname='client' user='roman' host='localhost' password='1234'")
			cursor = conn.cursor()
			
			#df = pd.read_sql_query("SELECT datetime, data, num_reg FROM iface_data WHERE datetime BETWEEN (date_trunc('hour', now()::timestamp) - INTERVAL '1 HOUR') AND date_trunc('hour', now()::timestamp)", conn)							
			#df2 = pd.pivot_table(df, index='datetime', columns='num_reg', values='data')									
			#df2.to_csv("/home/roman/data/data.csv", sep=';', header=None, float_format='%.0f')						
			
			
			cursor.execute(" SELECT datetime, data, num_reg FROM iface_data WHERE datetime BETWEEN (date_trunc('hour', now()::timestamp) - INTERVAL '2 HOUR') AND date_trunc('hour', now()::timestamp - INTERVAL '1 HOUR') ")		
			
			df = cursor.fetchall() #Получаем list				
			df2 = pd.DataFrame(df) #Конвертируем list в pandas dataframe
			df2.columns = ['datetime', 'data', 'num_reg']  #Добавляем заголовки		
			df3 = pd.pivot_table(df2, index='datetime', columns='num_reg', values='data') #Преобразуем таблицу													
			df3.to_csv("/home/roman/data/data.csv", sep=';', header=None, float_format='%.0f') 									
			
			
			conn.close()