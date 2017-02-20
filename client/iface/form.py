from django import forms
from .models import MainSettings, EthernetSettings, rs485Settings
from datetime import timedelta, datetime, tzinfo
from django.forms import ModelForm
from django.forms import fields 
 
class CheckBoxForm(forms.Form):
    #checkbox = forms.CharField(label='Your name', max_length=100)
    checkbox = forms.BooleanField
    
class MainSettingsForm(forms.ModelForm):
    
    user_login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин', 'required': 'true'}))
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'required': 'false'}))
    user_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля', 'required': 'true'}))
    period = forms.IntegerField(widget=forms.TimeInput(attrs={'placeholder': 'Секунды', 'required': 'true'}))
    datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': '2006-10-25 14:30:59', 'required': 'false'}))
    #sync_time = forms.BooleanField()
    sync_server = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'http://ntp2.stratum2.ru', 'required': 'true'}))    
    remote_server = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'http://ftp.example.com', 'required': 'false'}))    
    

    class Meta:
        model = MainSettings
        fields = '__all__'
        #fields = ['id_MainSettings', 'user_login', 'user_password', 'sync_time', 'sync_server', 'datetime', 'period', 'remote_server']
        
  
    
    #def clean(self):        
        # Определяем правило валидации
        #if self.cleaned_data.get('user_password') != self.cleaned_data.get('user_password_confirm'):
            # Выбрасываем ошибку, если пароли не совпали
            #raise forms.ValidationError({'user_password_confirm':'Пароли должны совпадать!'})       
            
        #return self.cleaned_data
        
        
class EthernetSettingsForm(forms.ModelForm):
    
    ip = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': '1.1.1.1', 'required': 'true'}))
    mask = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': '255.255.255.0', 'required': 'true'}))
    gateway = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': '192.168.0.1', 'required': 'true'}))
    dns = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': '8.8.8.8', 'required': 'false'}))
    
    class Meta:
       model = EthernetSettings
       fields = '__all__'
       
       
class rs485SettingsForm(forms.ModelForm):
            
    speed = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '11500', 'required': 'true'}))
    parity = forms.IntegerField()
    stop_bit = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '1', 'required': 'true'}))
    timeout = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '50', 'required': 'true'}))
    
    class Meta:
        model = rs485Settings
        fields = '__all__'
        
    