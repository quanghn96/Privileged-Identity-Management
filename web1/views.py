from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login,logout
from ssh.models import LoginInfo
from Location.models import Area, Ticket, AdminSSH, MessageTicket
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ipware import get_client_ip

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )
  
def get_client_ip(request):
    """get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]

    return ip
def index(request):
    aa = get_client_ip(request)
    return render(request, 'home.html',{'ip':aa,})

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request,user)
                LoginInfo.objects.create(user=user, ip=get_client_ip(request))
                request.session['username']= request.POST['username']
                request.session.set_expiry(300);
                return redirect('/')
        else:
        	return HttpResponse('fail')
    
    else:
    	loginrForm = LoginForm() 
    	return render(request, 'login.html', {'form':loginrForm})

def logoutUser(request):
    try:
        if request.session['username']:
            del request.session['username']
            logout(request)
            return redirect('/login')
    except:
        logout(request)
        return redirect('/')        
@login_required(login_url='/login') 
def ticket(request):
    if not request.user.is_staff or request.user.is_superuser:
        obj = Area.objects.all()
        return render(request, 'ticket.html',{'obj':obj,'idUser':request.user.id})
    else:
        return redirect('/')   

def addticket(request):
    try:
        idLocation = request.GET.get('idLocation','None')#id SSH connection
        message = request.GET.get('message','None')
        idUSer = request.GET.get('idUSer','None')
        t = request.GET.get('title','None')
        a = Area.objects.get(pk=idLocation)
        u = User.objects.get(id=idUSer)
        Ticket.objects.create(location=a, title=t, message=message, user=u)
        return JsonResponse({'id':'OK'})
    except:
        return JsonResponse({'id':t})                

@login_required(login_url='/login')
def message(request):
    if not request.user.is_staff or request.user.is_superuser:
        return redirect('/')
    else:
        try:
            u = AdminSSH.objects.get(admin=request.user)
            t = Ticket.objects.filter(location=u.location)
            return render(request, 'message.html',{'obj':t})   
        except:
            return render(request, 'message.html')   
@login_required(login_url='/login')
def viewMessage(request, id):
    try:
        t = Ticket.objects.get(pk=id)
        mt = MessageTicket.objects.filter(ticket__id=id)


        return render(request, 'viewMessage.html',{'obj':t, 'msg':mt})  
    except:
        return render(request, 'index.html') 

def AddMessage(request):
    try:
        idTicket = request.GET.get('idTicket','None')#id SSH connection
        message = request.GET.get('message','None')
        t = Ticket.objects.get(pk=idTicket)
        MessageTicket.objects.create(ticket=t, message=message, user = request.user)
        return JsonResponse({'id':'OK'})
    except:
        return JsonResponse({'id':'Fail'})  

def myTicket(request):
    try:
        t = Ticket.objects.filter(user=request.user)
        return render(request, 'myTicket.html', {'ticket':t}) 
    except:
        return render(request, 'index.html')            

# def viewMyTicket(request, id):
#     try:

#         return render(request, 'index.html')   
#     except:
#         return render(request, 'index.html')         