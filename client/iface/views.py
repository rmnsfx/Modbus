from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from .form import *
from .models import MainSettings


def main (request):

    return render_to_response('iface/main.html')

def conf (request):
    
    args = {}
    
    try:    
        
        main_settings = MainSettings.objects.get(pk=2)
    
    except MainSettings.DoesNotExist:   
        print('data model no exist')
        
    form = MainSettingsForm(request.POST, instance=main_settings) 
    
    if form.is_valid():      
            
            form.save()              
            print('!!! form valid')   
            
    else:
            print('form no valid', form.errors)
            
        
                
    return render_to_response('iface/conf.html', {'main_settings': form}, context_instance=RequestContext(request))
    #return render_to_response('iface/conf.html', RequestContext(request))    
    #return render(request, 'iface/conf.html', {'main_settings': form.errors})
    #return render_to_response('iface/conf.html', {'main_settings': main_settings})    
    
    
    
  
    
    
def data (request):

    return render_to_response('iface/data.html')