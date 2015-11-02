from django.conf.urls import patterns, url
 
from core import views
 
urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^api/login$', views.login, name='login'),
)
