# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import SSH, SSHPermission
# Register your models here.

class SSHAdmin(admin.ModelAdmin):
	list_display = ('ip', 'port','pub_date')

admin.site.register(SSH, SSHAdmin)
admin.site.register(SSHPermission)