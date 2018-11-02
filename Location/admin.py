from django.contrib import admin
from .models import Area,AdminSSH
# Register your models here.
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    birthday = models.DateField()

    def born_in_fifties(self):
        return self.birthday.strftime('%Y')[:3] == '195'
    born_in_fifties.boolean = True

class aSSHAdmin(admin.ModelAdmin):
	
	fieldsets = (
		('List Location',{
			'classes':('collapse'),
			'fields':('name','address')
			}),
	)

admin.site.register(Area, aSSHAdmin)
admin.site.register(AdminSSH)