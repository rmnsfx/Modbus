#!/usr/bin/python
# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from .form import *
from .models import MainSettings, EthernetSettings, rs485Settings
from django.contrib import messages
from datetime import datetime, timedelta
import time
from django.core.serializers.json import DjangoJSONEncoder
import json
import itertools
from datetime import date
import os 
from django.conf import settings
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import zipfile
import pandas as pd
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
import re
from django.forms.models import inlineformset_factory
import csv


def main (request):
   
    time_value = []
    reg1 = []
    reg2 = []
    reg3 = []
    reg4 = []
    reg5 = []
    reg6 = []
    reg7 = []
    reg8 = []
    
    
    timestr = datetime.now() - timedelta(hours=1)							
    outfilename = '{}.csv'.format(timestr.strftime("%Y-%m-%d_%H-00"))
    
    with open('/home/roman/data/' + outfilename, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            time_value.append(row[0])
            reg1.append(row[1])
            reg2.append(row[2])
            reg3.append(row[3])
            reg4.append(row[4])
            reg5.append(row[5])
            reg6.append(row[6])
            reg7.append(row[7])
            reg8.append(row[8])
        
    #Конвертируем string в float
    reg1 = [float(i) for i in reg1]
    reg2 = [float(i) for i in reg2]
    reg3 = [float(i) for i in reg3]
    reg4 = [float(i) for i in reg4]
    reg5 = [float(i) for i in reg5]
    reg6 = [float(i) for i in reg6]
    reg7 = [float(i) for i in reg7]
    reg8 = [float(i) for i in reg8]
    
    #reg1 = map(int, reg1)
    
    #raise 
    #time_value = list(time_value) 
    #time_data =  json.dumps(time_value, cls=DatetimeEncoder)    
    
    
    # df = pd.read_csv('/home/roman/data/' + outfilename, sep=';', names = ["datetime", "reg0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])                               
    # time_data = df.datetime.tolist()
    # reg1 = df.reg0.tolist()

    
    return render(request, 'iface/main.html', {'reg1': reg1, 'reg2': reg2, 'reg3': reg3, 'reg4': reg4, 'reg5': reg5, 'reg6': reg6, 'reg7': reg7, 'reg8': reg8, 'time': time_value })   

def conf (request):


    save_mes = False
    delete_button_flag = False
    cnt = 0
    error_message = False
    temp = None
 
            
    try:     
        
        #main_settings = MainSettings.objects.get(user_login__contains="roman")
        main_settings = MainSettings.objects.get(pk=1)
        ethernet_settings = EthernetSettings.objects.get(user_login_id=main_settings.pk)
        rs485_settings = rs485Settings.objects.get(user_login_id=main_settings.pk)
        #modbus_settings = ModbusSettings.objects.get(user_login_id=main_settings.pk)           
    
    except MainSettings.DoesNotExist:    
        #print('data model no exist')
        main_settings = None
        ethernet_settings = None
        rs485_settings = None
        modbus_settings = None
    
    form_main = MainSettingsForm(instance=main_settings) 
    form_ethernet = EthernetSettingsForm(instance=ethernet_settings)  
    form_rs485 = rs485SettingsForm(instance=rs485_settings)      
    #form_modbus = ModbusSettingsForm(instance=modbus_settings)

         
        

    if request.method == 'POST' and 'submit_main_form' in request.POST:
        
        form_main = MainSettingsForm(request.POST, instance=main_settings) 
        
        
        if form_main.is_valid():   
            
            form_main.save()
            
            save_mes = True 
            
        else:
            
            print('main_form no valid')
            print(form_main.errors)
    
    #else: form_main = None 
            
    if request.method == 'POST' and 'submit_ethernet_form' in request.POST:    
                        
        form_ethernet = EthernetSettingsForm(request.POST, instance=ethernet_settings)
        
        form_ethernet.user_login_id = main_settings.pk
        
        #form_ethernet.fields['user_login'] = ethernet_settings.user_login_id
                        
        if form_ethernet.is_valid():    
        
            form_ethernet.save()
            
            save_mes = True 
            
        else:
            
            print('ethernet_form no valid')         
    
    #else: form_ethernet = None     
        
    if request.method == 'POST' and 'submit_rs485_form' in request.POST:
        
        form_rs485 = rs485SettingsForm(request.POST, instance=rs485_settings)
        
        form_rs485.user_login_id = main_settings.pk
        
        
        if form_rs485.is_valid():
    
            form_rs485.save()
            
            save_mes = True 
            
        else:
            
            print('rs485_form no valid')
            print(form_rs485.errors)
            
    #else: form_rs485 = None        
    
    
    
    formset = modelformset_factory(ModbusSettings, exclude=('user_login',), extra=0)           
    prims = formset    
    
    
        
    
    #Добавляем форму в набор (пустое поле)
    if request.method == 'POST' and 'add_reg' in request.POST:  
        
        prims = formset(request.POST)
        
        cp = request.POST.copy()
        cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) + 1
        prims = formset(cp,prefix='form')
        
    
    
    #Определяем нажатие кнопки удаления
    for key in request.POST:
        if 'delete_button' in key:
            delete_button_flag = True    
    
    if request.method == 'POST' and delete_button_flag:     
        
        prims = formset(request.POST)        
        
        
		#Определяем индекc нажатой кнопки
        for i in range(0, prims.total_form_count() + 1):        
            if 'delete_button_' + str(i) in request.POST:   
                cnt = i - 1    
                       
        
        
        
        #Удаляем из бд
        try:
            prims[cnt].instance.delete()
            
            # # form_for_delete = prims[cnt]        
            # # id = form_for_delete['id_ModbusSettings'].value()        
            # # ModbusSettings.objects.get(id_ModbusSettings=id).delete()
        
        except:
            error_message = True


        
        #Обновляем набор форм (формсет) 
        prims = modelformset_factory(ModbusSettings, exclude=('user_login',), extra=0)       

    #Сохраняем изменения в бд
    if request.method == 'POST' and 'edit' in request.POST:
        
        FormSet = modelformset_factory(ModbusSettings, exclude=('user_login',), extra=0)        
        data = request.POST or None
        formset = FormSet(data=data)
        
        if formset.is_valid():
            
            formset.save()            
            save_mes = True             

        else:
            
            print('modbus_form no valid')
            print(prims.errors)
                
        
    
    
    
        
    return render(request, 'iface/conf.html', {'main_settings': form_main, 'ethernet_settings': form_ethernet, 'rs485_settings': form_rs485, 'modbus_settings' : prims, 'save_mes': save_mes, 'temp' : temp} )        
        
    
    
def data (request):

    #form_arch = ArchForm(request.POST)
    
    path="/home/roman/data/" 
    link = os.listdir(path)
    link.sort(reverse=True) 
    
    if request.method == 'POST' and 'submit_data_form' in request.POST:
    
        zf = zipfile.ZipFile("/home/roman/zipdata.zip", "w")
        
        for dirs, subdirs, files in os.walk('/home/roman/data/'):
        
            #zf.write(dirname)
            for f in files:             
                zf.write(os.path.join("/home/roman/data/",f))

        zf.close()
        
        f = open('/home/roman/zipdata.zip', 'rb')
        
        response = HttpResponse(f, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="zipdata.zip"'
        
        return response
    
    
    return render(request, 'iface/data.html', {'link': link })  
    #return render(request, 'iface/data.html', {'form_arch': form_arch })       
    #return HttpResponseRedirect("")
    
    
    
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
    
    

