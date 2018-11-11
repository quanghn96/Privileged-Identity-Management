# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from Location.models import Area

class SSH(models.Model):

	ip = models.CharField(max_length=15,null=True)
	port = models.IntegerField(default=22,null=True)
	username = models.CharField(max_length=100,null=True)
	password = models.CharField(max_length=100,null=True)
	pub_date = models.DateTimeField(default=timezone.now)
	area = models.ForeignKey('Location.Area',on_delete=models.CASCADE) 
	def __str__(self):
		return self.ip
class SSHPermission(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)	
	sshconnection = models.ManyToManyField(SSH)
	permission = models.BooleanField(default=False)
	def __str__(self):
		return self.user.username

# class statusSSH(models.Model):
# 	connection = models.ForeignKey(SSH, on_delete=models.CASCADE, primary_key=True)
# 	status = models.BooleanField(default=False)
# 	def __str__(self):
# 		return self.connection.ip

class BlackList(models.Model):
	keyword = models.CharField(max_length=100, unique=True)
	def __str__(self):
		return self.keyword

class TimeBlackList(models.Model):
	list = models.ManyToManyField(BlackList)
	ssh = models.ForeignKey(SSH, on_delete=models.CASCADE, unique=True)
	startTime = models.TimeField(auto_now=False, auto_now_add=False)
	endTime = models.TimeField(auto_now=False, auto_now_add=False)

class LoginInfo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ip = models.CharField(max_length=15,null=True)
	logTime = models.DateTimeField(default=timezone.now)

class LogCommand(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	connection = models.ManyToManyField(SSH)
	logTime = models.DateTimeField(default=timezone.now)
	command = models.TextField(max_length=1000)

class AccessSSH(models.Model):
	ssh = models.OneToOneField(SSH, on_delete=models.CASCADE)