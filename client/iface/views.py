from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from .form import *
from .models import MainSettings, EthernetSettings, rs485Settings
from django.contrib import messages


def main (request):

	return render_to_response('iface/main.html')

def conf (request):
			
	#try:	 
		
	#main_settings = MainSettings.objects.get(user_login__contains="roman")
	main_settings = MainSettings.objects.get(pk=1)
	ethernet_settings = EthernetSettings.objects.get(user_login_id=main_settings.pk)
	rs485_settings = rs485Settings.objects.get(user_login_id=main_settings.pk)
	
	#except MainSettings.DoesNotExist:	 
		#print('data model no exist')	  

	var_mes = False 
	
	form_main = MainSettingsForm(instance=main_settings) 
	form_ethernet = EthernetSettingsForm(instance=ethernet_settings)  
	form_rs485 = rs485SettingsForm(instance=rs485_settings)		 
	
	

	if request.method == 'POST' and 'submit_main_form' in request.POST:
		
		form_main = MainSettingsForm(request.POST, instance=main_settings) 
		
		if form_main.is_valid():   
			
			form_main.save()
			
			var_mes = True 
			
		else:
			
			print('main_form no valid')
			print(form_main.errors)
			
			
	if request.method == 'POST' and 'submit_ethernet_form' in request.POST:	   
						
		form_ethernet = EthernetSettingsForm(request.POST, instance=ethernet_settings)
		
		form_ethernet.user_login_id = main_settings.pk
		
		#form_ethernet.fields['user_login'] = ethernet_settings.user_login_id
						
		if form_ethernet.is_valid():	
		
			form_ethernet.save()
			
			var_mes = True 
			
		else:
			
			print('ethernet_form no valid')			
			
		
	if request.method == 'POST' and 'submit_rs485_form' in request.POST:
		
		form_rs485 = rs485SettingsForm(request.POST, instance=rs485_settings)
		
		form_rs485.user_login_id = 1
		
		
		if form_rs485.is_valid():
	
			form_rs485.save()
			
			var_mes = True 
			
		else:
			
			print('rs485_form no valid')
			print(form_rs485.errors)
		

		
	return render(request, 'iface/conf.html', {'main_settings': form_main, 'ethernet_settings': form_ethernet, 'rs485_settings': form_rs485, 'var_mes': var_mes})	  
	#return render_to_response('iface/conf.html', {'main_settings': form_main}, context_instance=RequestContext(request))
	
	
	
	
  
	
	
def data (request):

	return render_to_response('iface/data.html')