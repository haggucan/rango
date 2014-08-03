from django.conf.urls import patterns, url
from rangotest import views

urlpatterns = patterns('',
                       url(r'^$', views.about, name='about'),)
