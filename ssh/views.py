from django.http import HttpResponse
from .models import SSHPermission ,SSH
from django.template import loader
from django.shortcuts import render, get_object_or_404
import paramiko

def index(request):
	if request.user.is_authenticated():
		try:
			obj = get_object_or_404(SSHPermission, user__username=request.user.username)
			context = {'obj':obj,}
		except SSHPermission.DoesNotExist:
			context = None	
		return render(request, 'index.html', context)			
	else:
		return render(request,'index.html')	

def detail(request, id):
	return render(request,'detail.html')	