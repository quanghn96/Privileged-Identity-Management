from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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

class Ticket(models.Model):
	location = models.ForeignKey(Area,on_delete=models.CASCADE)
	title = models.CharField(max_length=1000, default="")
	message = models.CharField(max_length=1000)
	user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
	time = models.DateTimeField(default=timezone.now)

class MessageTicket(models.Model):
	ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
	message = models.CharField(max_length=1000)	
	user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
	time = models.DateTimeField(default=timezone.now)