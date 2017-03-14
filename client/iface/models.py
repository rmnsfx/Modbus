#!/usr/bin/python
# coding: utf-8
from django.db import models
from datetime import timedelta, datetime, tzinfo
from django.utils import timezone



class MainSettings(models.Model):

	id_MainSettings = models.AutoField(primary_key=True)
	user_login = models.CharField(max_length=50, null=False, unique=True)
	user_password = models.CharField(max_length=50, null=True)	  
	datetime = models.DateTimeField(null=True)
	sync_time = models.BooleanField()
	sync_server = models.URLField(null=True)
	period = models.IntegerField(null=True)
	remote_server = models.URLField(null=True)
	change_datetime = models.DateTimeField(auto_now=True, null=True)


class EthernetSettings(models.Model):
	
	id_EthernetSettings = models.AutoField(primary_key=True)
	user_login = models.ForeignKey(MainSettings, default=0)
	ip = models.GenericIPAddressField(max_length=50, null=True)
	mask = models.GenericIPAddressField(max_length=50, null=True)
	gateway = models.GenericIPAddressField(max_length=50, null=True)
	dns = models.GenericIPAddressField(max_length=50, null=True)
	
	
class rs485Settings(models.Model):
	
	id_rs485Settings = models.AutoField(primary_key=True)
	user_login = models.ForeignKey(MainSettings, default=0)
	speed = models.IntegerField(null=True)
	parity = models.IntegerField(null=True)
	stop_bit = models.IntegerField(null=True)
	timeout = models.IntegerField(null=True)
	

class ModbusSettings(models.Model):

	id_ModbusSettings = models.AutoField(primary_key=True)
	user_login = models.ForeignKey(MainSettings, default=0)
	adr_item = models.IntegerField(null=True)
	type_reg = models.IntegerField(null=True)
	index_reg = models.IntegerField(null=True)
	type_data = models.IntegerField(null=True)
	size = models.IntegerField(null=True)
	multiplier = models.IntegerField(null=True)
	tag = models.CharField(max_length=50, null=True)	
	archiving = models.BooleanField()
	
class Data(models.Model):

	id_Data = models.AutoField(primary_key=True)
	user_login = models.ForeignKey(MainSettings, default=0)
	data = models.IntegerField(null=True)
	datetime = models.DateTimeField(auto_now_add=True, null=True)
	#module_number = models.IntegerField(null=True)
	#pid = models.IntegerField(null=True)
	num_reg = models.IntegerField(null=True)
	
	