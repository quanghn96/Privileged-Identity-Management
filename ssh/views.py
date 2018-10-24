from django.http import HttpResponse
from .models import SSHPermission ,SSH
from django.template import loader
from django.shortcuts import render, get_object_or_404
import paramiko
from django.http import JsonResponse


def index(request):
	if not request.user.is_superuser:
		try:
			obj = get_object_or_404(SSHPermission, user__username=request.user.username)
			context = {'obj':obj,}
		except :
			context = None	
		return render(request, 'index.html', context)			
	else:
		return render(request,'index.html')	

def detail(request, id):
	if not request.user.is_superuser:
		try:
			getSSH = SSH.objects.filter(sshpermission__user__username=request.user.username,sshpermission__permission=True)
			obj = get_object_or_404(getSSH, id=id)
			context = {'obj':obj}
		except SSHPermission.DoesNotExist:
			context = None	
		return render(request, 'detail.html', context)			
	else:
		return render(request,'detail.html')	

def connect(request, id):
	try:
		obj = get_object_or_404(SSH,pk=id)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(obj.ip, obj.port, username=obj.username,password=obj.password)
		data = {
			'status':'Connect successfully',
			'code':1
		}
	except:
		data = {
			'status':"Can't connect",
			'code':0
		}
	return JsonResponse(data)		

def disconnect(request, id):
	if ssh:
		ssh.close()
