from django.conf.urls import url 
from . import views 

app_name = "ssh" 
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
]