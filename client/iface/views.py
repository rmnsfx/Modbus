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
        
    main_settings = MainSettings.objects.get(pk=1)
    ethernet_settings = EthernetSettings.objects.get(pk=1)
    rs485_settings = rs485Settings.objects.get(pk=1)
    
    #except MainSettings.DoesNotExist:   
        #print('data model no exist')
    
    var_mes = True  
    
    form_main = MainSettingsForm(instance=main_settings) 
    form_ethernet = EthernetSettingsForm(instance=ethernet_settings)  
    form_rs485 = rs485SettingsForm(instance=rs485_settings)  

    if request.method == 'POST':
    
        if form_main.is_valid():      
                                                  
            form_main.save()
            
                
        else:
            
            print('form no valid')
                
            
        

    return render(request, 'iface/conf.html', {'main_settings': form_main, 'ethernet_settings': form_ethernet, 'rs485_settings': form_rs485, 'var_mes': var_mes})     
    #return render_to_response('iface/conf.html', {'main_settings': form_main}, context_instance=RequestContext(request))
    
    
    
    
  
    
    
def data (request):

    return render_to_response('iface/data.html')