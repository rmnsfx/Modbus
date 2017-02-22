from django.contrib import admin
from .models import *

admin.site.register(MainSettings)
admin.site.register(EthernetSettings)
admin.site.register(rs485Settings)