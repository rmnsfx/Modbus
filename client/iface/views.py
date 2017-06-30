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
import time
import os 
from django.conf import settings
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import zipfile
import pandas as pd
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
import re



def main (request):

	#array = Data.objects.filter(num_reg=4).values_list('data', flat=True)		
	#array = Data.objects.values_list('data', flat=True).order_by('-data')[:100][::-1]
	
	# start_time = time.time()
	# end_time = time.time()					
	# timr = end_time - start_time
		
	time_1_hour_ago = datetime.now() - timedelta(hours = 1)
	
	reg1 = Data.objects.filter( num_reg=1, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)				
	#reg1 = Data.objects.filter( num_reg=1, datetime__gt = date.today() ).values_list('data', flat=True)				
	reg1 = list(reg1)
	
	#time_value = Data.objects.values_list('datetime', flat=True)
	
	time_value = Data.objects.filter( num_reg=1, datetime__gte = time_1_hour_ago ).values_list('datetime', flat=True)	
	#time_value = Data.objects.filter( num_reg=1, datetime__gt = date.today() ).values_list('datetime', flat=True)	
	time_value = list(time_value)	
	#time_data =	 json.dumps(time_value, cls=DatetimeEncoder)
	
	time_data =	 json.dumps(time_value, cls=DatetimeEncoder)	

	#raise(timr)
	
	# reg2 = Data.objects.filter( num_reg=2, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	# reg3 = Data.objects.filter( num_reg=3, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	# reg4 = Data.objects.filter( num_reg=4, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	# reg5 = Data.objects.filter( num_reg=5, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	# reg6 = Data.objects.filter( num_reg=6, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	# reg7 = Data.objects.filter( num_reg=7, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	# reg8 = Data.objects.filter( num_reg=8, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	# reg9 = Data.objects.filter( num_reg=9, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	# reg10 = Data.objects.filter( num_reg=10, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	# reg11 = Data.objects.filter( num_reg=11, datetime__gte = time_1_hour_ago ).values_list('data', flat=True)			
	
	# reg2 = list(reg2)
	# reg3 = list(reg3)
	# reg4 = list(reg4)
	# reg5 = list(reg5)
	# reg6 = list(reg6)
	# reg7 = list(reg7)
	# reg8 = list(reg8)
	# reg9 = list(reg9)
	# reg10 = list(reg10)
	# reg11 = list(reg11)	
	
	
	df = pd.read_csv('/home/roman/data/data.csv', sep=';', names = ["datetime", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])						   
	
	
	# df = cursor.fetchall() #Получаем list				
	# df2 = pd.DataFrame(df) #Конвертируем list в pandas dataframe
	# df2.columns = ['datetime', 'data', 'num_reg']  #Добавляем заголовки		
	# df3 = pd.pivot_table(df2, index='datetime', columns='num_reg', values='data') #Преобразуем таблицу													
	# df3.to_csv("/home/roman/data/data.csv", sep=';', header=None, float_format='%.0f') 						
			
	
	
	# return render(request, 'iface/main.html', {'reg1': reg1, 'time': time_data, 'reg2': reg2, 'reg3': reg3, 'reg4': reg4, 'reg5': reg5,'reg6': reg6,'reg7': reg7,'reg8': reg8,'reg9': reg9,'reg10': reg10,'reg11': reg11})
	
	return render(request, 'iface/main.html', {'reg1': reg1, 'time': time_data })	

def conf (request):	
			
#try:	 
	
	#main_settings = MainSettings.objects.get(user_login__contains="roman")
	main_settings = MainSettings.objects.get(pk=1)
	ethernet_settings = EthernetSettings.objects.get(user_login_id=main_settings.pk)
	rs485_settings = rs485Settings.objects.get(user_login_id=main_settings.pk)
	modbus_settings = ModbusSettings.objects.get(user_login_id=main_settings.pk)			
	
#except MainSettings.DoesNotExist:	 
	#print('data model no exist')
	#main_settings = None
	#ethernet_settings = None
	#rs485_settings = None
	#modbus_settings = None
	
	form_main = MainSettingsForm(instance=main_settings) 
	form_ethernet = EthernetSettingsForm(instance=ethernet_settings)  
	form_rs485 = rs485SettingsForm(instance=rs485_settings)		 
	form_modbus = ModbusSettingsForm(instance=modbus_settings)

	save_mes = False 
	
	

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
	
	
	
	
	
	#formset = modelformset_factory(ModbusSettings, fields=('id_ModbusSettings', 'adr_item', 'type_reg', 'index_reg', 'type_data', 'size', 'multiplier', 'tag'))
	#formset = modelformset_factory(ModbusSettings, form=ModbusSettingsForm)		
	#formset = formset_factory(ModbusSettingsForm)
	
	formset = modelformset_factory(ModbusSettings, exclude=('user_login',), can_delete=True)	
	
	prims = formset
		
	if request.method == 'POST' and 'add_reg' in request.POST:	
		
		prims = formset(request.POST)
		
		cp = request.POST.copy()
		cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) + 1
		prims = formset(cp,prefix='form')
		
		
	if request.method == 'POST' and 'del_reg' in request.POST:	
		
		prims = formset(request.POST)
	
		#id = 24
		
		cp = request.POST.copy()
		cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) - 1
		prims = formset(cp,prefix='form')
		
		# instances = prims.save(commit=False)
		
		# for obj in prims.deleted_objects:
			# obj.delete()
			
		#ModbusSettings.objects.get(id_ModbusSettings=id).delete()
		

	if request.method == 'POST' and 'submit_modbus_form' in request.POST:
		
		prims = formset(request.POST)
		
		#form_modbus = ModbusSettingsForm(request.POST, instance=modbus_settings)		
		#form_modbus.user_login_id = main_settings.pk		
		#if form_modbus.is_valid():
		
		if prims.is_valid():
					
			prims.save()					
				
			save_mes = True

				

		else:
			
			print('modbus_form no valid')
			print(form_modbus.errors)
	
	#else: form_modbus = None	
		
	#if request.method == 'POST' and  in request.POST:
		
		#save_mes = True
		
	
	if request.method == 'POST' and 'edit' in request.POST:
		
		ProductFormSet = modelformset_factory(ModbusSettings, exclude=('user_login',), can_delete=True)		
		data = request.POST or None
		formset = ProductFormSet(data=data)
		
		formset.save()
			
	
	
	
		
	return render(request, 'iface/conf.html', {'main_settings': form_main, 'ethernet_settings': form_ethernet, 'rs485_settings': form_rs485, 'modbus_settings' : prims, 'save_mes': save_mes})		
		
	#return render(request, 'iface/conf.html', {'main_settings': form_main, 'ethernet_settings': form_ethernet, 'rs485_settings': form_rs485, 'modbus_settings' : form_modbus,'save_mes': save_mes, 'loop_times':loop_times})	  
	#return render_to_response('iface/conf.html', {'main_settings': form_main}, context_instance=RequestContext(request))
	
	
	
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
	
	

