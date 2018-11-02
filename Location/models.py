from django.db import models
from django.contrib.auth.models import User
class Area(models.Model):
	name = models.CharField(max_length=100,null=True)
	address = models.CharField(max_length=100,null=True)
	def __str__(self):
		return self.name

class AdminSSH(models.Model):
	location = models.ForeignKey(Area,on_delete=models.CASCADE, primary_key=True)
	admin = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.admin.username