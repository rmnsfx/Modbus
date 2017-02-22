from django import forms
from .models import *
from datetime import timedelta, datetime, tzinfo
from django.forms import ModelForm
from django.forms import fields 

	
class MainSettingsForm(forms.ModelForm):
	
	user_login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин', 'required': 'true'}))
	user_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'required': 'true'}))
	user_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля', 'required': 'true'}))
	period = forms.IntegerField(widget=forms.TimeInput(attrs={'placeholder': 'Секунды', 'required': 'true', 'pattern':'[0-9]'}))
	datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': '2006-10-25 14:30:59'}))
	sync_time = forms.BooleanField(widget=forms.CheckboxInput(), required=False, initial=True)
	sync_server = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'http://ntp2.stratum2.ru'}))	  
	remote_server = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'http://ftp.example.com' }))	
	

	class Meta:
		model = MainSettings
		fields = '__all__'
		#fields = ['id_MainSettings', 'user_login', 'user_password', 'sync_time', 'sync_server', 'datetime', 'period', 'remote_server'] 
	
	def clean(self):		 
		# Определяем правило валидации
		if self.cleaned_data.get('user_password') != self.cleaned_data.get('user_password_confirm'):
			# Выбрасываем ошибку, если пароли не совпали
			raise forms.ValidationError({'user_password_confirm':'Пароли должны совпадать!'})		 
			
		return self.cleaned_data
		
		
class EthernetSettingsForm(forms.ModelForm):
	
	ip = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': '1.1.1.1', 'required': 'true'}))
	mask = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': '255.255.255.0', 'required': 'true'}))
	gateway = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': '192.168.0.1', 'required': 'true'}))
	dns = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': '8.8.8.8', 'required': 'false'}))
	
	class Meta:
		model = EthernetSettings		
		exclude = ['user_login']	   
		
	   
	   
	   
class rs485SettingsForm(forms.ModelForm):
		
	speed = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '11500', 'required': 'true'}))
	parity = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:default%'}), choices=(('1', 'Четность'), ('2', 'Нечетность')))
	stop_bit = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '1', 'required': 'true'}))
	timeout = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '50', 'required': 'true'}))
	
	class Meta:
		model = rs485Settings		
		exclude = ['user_login']
		
	
	
class ModbusSettingsForm(forms.ModelForm):	
		
	adr_item = forms.IntegerField(widget=forms.TextInput(attrs={'required': 'true'}))
	typr_reg = forms.IntegerField(widget=forms.TextInput(attrs={'required': 'true'}))
	index_reg = forms.IntegerField(widget=forms.TextInput(attrs={'required': 'true'}))
	type_data = forms.IntegerField(widget=forms.TextInput(attrs={'required': 'true'}))
	size = forms.IntegerField(widget=forms.TextInput(attrs={'required': 'true'}))
	multiplier = forms.IntegerField(widget=forms.TextInput(attrs={'required': 'true'}))
	tag = forms.CharField(widget=forms.TextInput(attrs={'required': 'true'}))	   
	archiving = forms.BooleanField(widget=forms.TextInput(attrs={'required': 'false'}))
	
	class Meta:
		model = ModbusSettings		
		exclude = ['user_login']