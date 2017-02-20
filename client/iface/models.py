from django.db import models
from datetime import timedelta, datetime, tzinfo
from django.utils import timezone



class MainSettings(models.Model):
    id_MainSettings = models.AutoField(primary_key=True)
    user_login = models.CharField(max_length=50, null=True, unique=True)
    user_password = models.CharField(max_length=50, null=True)
    #user_password_confirm = models.CharField(max_length=50, null=True, blank=False)
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
    parity = models.IntegerField(choices=((1, "Not relevant"), (2, "Review")) )
    stop_bit = models.IntegerField(null=True)
    timeout = models.IntegerField(null=True)