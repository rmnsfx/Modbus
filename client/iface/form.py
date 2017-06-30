#!/usr/bin/python
# coding: utf-8
from django import forms
from .models import *
from datetime import timedelta, datetime, tzinfo
from django.forms import ModelForm
from django.forms import fields 
import datetime
import time
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form
from django.contrib.admin.widgets import AdminDateWidget

	
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
		exclude = ['change_datetime']		
		#fields = '__all__'
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
	
	#id_ModbusSettings = forms.IntegerField(widget = forms.HiddenInput())	
	adr_item = forms.IntegerField(widget=forms.TextInput())
	type_reg = forms.IntegerField(widget=forms.TextInput())
	index_reg = forms.IntegerField(widget=forms.TextInput())
	type_data = forms.IntegerField(widget=forms.TextInput())
	size = forms.IntegerField(widget=forms.TextInput())
	multiplier = forms.IntegerField(widget=forms.TextInput())
	tag = forms.CharField(widget=forms.TextInput())	   	
	archiving = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
	
	class Meta:
		model = ModbusSettings
		widgets = {'id_ModbusSettings': forms.HiddenInput()}		
		exclude = ['user_login']
		
class ArchForm(forms.Form):	
	
	#date_field = forms.DateField(widget=SelectDateWidget(attrs={'class':'data'}))
	#time_field = forms.TimeField(widget=SelectTimeWidget())
	#datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': '2006-10-25 14:30:59'}))
	#from_time = forms.TimeField(widget=SelectTimeWidget(attrs={'class':'data'}), initial=datetime.now(), required=False)
	#t = forms.TimeField(widget=SelectTimeWidget())
	#date_posted = forms.DateTimeField(widget = forms.widgets.SplitDateTimeWidget(attrs={'class':'data'}))
	datetime_start = forms.DateTimeField(label="", widget=forms.DateTimeInput(attrs={'placeholder': '2006-10-25 14:30:59', 'class':'data'}), required=False)
	datetime_end = forms.DateTimeField(label="", widget=forms.DateTimeInput(attrs={'placeholder': '2006-10-25 14:30:59', 'class':'data'}), required=False)