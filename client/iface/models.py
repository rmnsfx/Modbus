from django.db import models
from datetime import timedelta, datetime, tzinfo
from django.utils import timezone



class MainSettings(models.Model):
    id_MainSettings = models.AutoField(primary_key=True)
    user_login = models.CharField(max_length=50, null=True, unique=True, blank=False)
    user_password = models.CharField(max_length=50, null=True, blank=False)
    user_password_confirm = models.CharField(max_length=50, null=True, blank=False)
    datetime = models.DateTimeField(null=True)
    sync_time = models.BooleanField()
    sync_server = models.URLField(null=True)
    period = models.IntegerField(null=True)
    remote_server = models.URLField(null=True)
    
    # def __str__(self):
        # return self.name

