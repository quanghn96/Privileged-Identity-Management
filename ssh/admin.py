# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import SSH, SSHPermission, LoginInfo, BlackList, LogCommand, AccessSSH, TimeBlackList, GrantHistory

# Register your models here.

class SSHAdmin(admin.ModelAdmin):
	list_display = ('ip', 'port','pub_date')

admin.site.register(SSH, SSHAdmin)
admin.site.register(SSHPermission)
admin.site.register(LoginInfo)
admin.site.register(BlackList)
admin.site.register(LogCommand)
admin.site.register(AccessSSH)
admin.site.register(TimeBlackList)
admin.site.register(GrantHistory)