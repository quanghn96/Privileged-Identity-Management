from django.http import HttpResponse
from .models import SSHPermission ,SSH
from Location.models import Area, AdminSSH
from django.template import loader
from django.shortcuts import render, get_object_or_404
import paramiko
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers


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

@login_required(login_url='/login')	
def manage(request):
	
	try:#Get admin's location
		getLocation = get_object_or_404(AdminSSH, admin__username=request.user.username)
		#GEt all connection with admin's location
		getSSH = SSH.objects.filter(area__id=getLocation.location.id)
		
		context ={
		'object':getSSH
		}
	except:
		return render(request, 'manage.html')
	return render(request, 'manage.html',context)	

def get_User(request):
	id = request.GET.get('id','None')#id SSH connection
	try:#List user is allow using connection with that id
		getObj = User.objects.filter(sshpermission__permission=True, sshpermission__sshconnection__pk=id)

	except:
		return JsonResponse({'id':'Fail !'})
	return JsonResponse(serializers.serialize('json', getObj, fields=('id', 'username')),  safe=False)	
#Need to fix Delete Object SSHPermission
def delete_User(request):
	idUser = request.GET.get('idUser','None')#id user
	idSSH = request.GET.get('idSSH','None')#id SSH connection
	try:#List user is allow using connection with that id
		s = SSH.objects.get(pk=idSSH)
		p = SSHPermission.objects.get(user__pk=idUser)
		p.sshconnection.remove(s)
		getObj = User.objects.filter(sshpermission__permission=True, sshpermission__sshconnection=idSSH)
	except:
		return JsonResponse({'id':'Fail11'+idUser+' - '+idSSH})
	return JsonResponse(serializers.serialize('json', getObj, fields=('id', 'username')),  safe=False)	

def add_User(request):
	username = request.GET.get('username','None')#id user
	idSSH = request.GET.get('idSSH','None')#id SSH connection
	try:#List user is allow using connection with that id
		usr = get_object_or_404(User,username=username)
		s = get_object_or_404(SSH, pk=idSSH)
		obj, created = SSHPermission.objects.get_or_create(user = usr)
		if created:# user has just created
			obj.sshconnection = s
			obj.permission = True
			return JsonResponse({'id':'created'})
		else:#Check whether this connection is already added ?
			getP = SSHPermission.objects.filter(user = obj.user, sshconnection = s)
			if getP:# user has created already
				return JsonResponse({'id':'User has been added already'})
			else:
				obj.sshconnection.add(s)
				obj.save()
				return JsonResponse({'id':'User has been added'})


	except:
		return JsonResponse({'id':'Fail to add username'})
	return JsonResponse({'id':'Add ok'})	

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
