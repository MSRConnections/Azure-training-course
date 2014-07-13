from django.conf.urls import patterns, include, url
from DjangoApplication.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoApplication.views.home', name='home'),
    # url(r'^DjangoApplication/', include('DjangoApplication.DjangoApplication.urls')),
    url('^earthquake/$',earthquake, name='earthquake'),   
    url(r'^$', home, name='home'),
    url(r'^webjob/(?P<latitude>-*\d*\.?\d+)/(?P<longitude>-*\d*\.?\d+)/$', webjob, name='webjob'),
    url(r'^result/(?P<latitude>-*\d*\.?\d+)/(?P<longitude>-*\d*\.?\d+)/$', result, name='result'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) 

urlpatterns += staticfiles_urlpatterns()  
