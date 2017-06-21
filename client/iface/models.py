#!/usr/bin/python
# coding: utf-8
from django.db import models
from datetime import timedelta, datetime, tzinfo
from django.utils import timezone



class MainSettings(models.Model):

	id_MainSettings = models.AutoField(primary_key=True)
	user_login = models.CharField(max_length=50, null=False, unique=True)
	user_password = models.CharField(max_length=50, null=False)	  
	datetime = models.DateTimeField(null=False)
	sync_time = models.BooleanField()
	sync_server = models.URLField(null=False)
	period = models.IntegerField(null=False)
	remote_server = models.URLField(null=False)
	change_datetime = models.DateTimeField(auto_now=True, null=False)


class EthernetSettings(models.Model):
	
	id_EthernetSettings = models.AutoField(primary_key=True)
	user_login = models.ForeignKey(MainSettings, default=0, null=False)
	ip = models.GenericIPAddressField(max_length=50, null=False)
	mask = models.GenericIPAddressField(max_length=50, null=False)
	gateway = models.GenericIPAddressField(max_length=50, null=False)
	dns = models.GenericIPAddressField(max_length=50, null=False)
	
	
class rs485Settings(models.Model):
	
	id_rs485Settings = models.AutoField(primary_key=True)
	user_login = models.ForeignKey(MainSettings, default=0, null=False)
	speed = models.IntegerField(null=False)
	parity = models.IntegerField(null=False)
	stop_bit = models.IntegerField(null=False)
	timeout = models.IntegerField(null=False)
	

class ModbusSettings(models.Model):

	id_ModbusSettings = models.AutoField(primary_key=True)
	user_login = models.ForeignKey(MainSettings, default=0, null=False)
	adr_item = models.IntegerField(null=False)
	type_reg = models.IntegerField(null=False)
	index_reg = models.IntegerField(null=False)
	type_data = models.IntegerField(null=False)
	size = models.IntegerField(null=False)
	multiplier = models.IntegerField(null=False)
	tag = models.CharField(max_length=50, null=False)	
	archiving = models.BooleanField()
	
class Data(models.Model):

	
	datetime = models.DateTimeField(auto_now_add=True, null=False)
	data = models.IntegerField(null=False)
	num_reg = models.IntegerField(null=False)
	user_login = models.ForeignKey(MainSettings, default=0, null=False)	
	id_data = models.AutoField(primary_key=True)
	#module_number = models.IntegerField(null=True)
	#pid = models.IntegerField(null=True)
	
	
	