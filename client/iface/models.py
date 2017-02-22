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
    
    # def __str__(self):
        # return self.name

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
	typr_reg = models.IntegerField(null=True)
	index_reg = models.IntegerField(null=True)
	type_data = models.IntegerField(null=True)
	size = models.IntegerField(null=True)
	multiplier = models.IntegerField(null=True)
	tag = models.CharField(max_length=50, null=True)    
	archiving = models.BooleanField()
	

	
	
	