from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from facebook_hack import views

# urlpatterns = patterns('',
#     url(r'^/api/login$', views.login, name='login'),
# )


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^api/login$', views.login, name='login'),
)
