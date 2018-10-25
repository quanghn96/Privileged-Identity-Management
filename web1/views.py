from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect

def index(request):
	return render(request, 'home.html')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('/')
        else:
        	return HttpResponse('fail')
    
    else:
    	loginrForm = LoginForm() 
    	return render(request, 'login.html', {'form':loginrForm})

def logoutUser(request):
    logout(request)
    return redirect('/login')