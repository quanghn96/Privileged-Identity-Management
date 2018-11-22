from django.conf.urls import url 
from . import views 

app_name = "ssh" 
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<id>[0-9]+)/connect$', views.connect, name='connectSSH'),
	url(r'^manage/', views.manage, name='manage'),
	url(r'^monitor/(?P<id>[0-9]+)$', views.monitor, name='monitor'),
	url(r'^log/(?P<id>[0-9]+)$', views.logSSH, name='logSSH'),
	url(r'^ajax/get_User/$', views.get_User, name='get_User'),\
	url(r'^ajax/delete_User/$', views.delete_User, name='delete_User'),
	url(r'^ajax/add_User/$', views.add_User, name='add_User'),
	url(r'^ajax/getTimeCommand/$', views.getTimeCommand, name='getTimeCommand'),
	url(r'^ajax/setTimeCommand/$', views.setTimeCommand, name='setTimeCommand'),
	url(r'^ajax/viewLog/$', views.viewLog, name='viewLog'),
	url(r'^ajax/viewLogUser/$', views.viewLogUser, name='viewLogUser'),
    # ex: /polls/5/results/
]