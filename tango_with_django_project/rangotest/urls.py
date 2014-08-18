from django.conf.urls import patterns, url
from rangotest import views

urlpatterns = patterns('',
                       url(r'^test/$', views.about, name='about'),
                       url(r'^$', views.about, name='about'),
                       url(r'^upload/$', views.upload, name='upload'),
                       url(r'^dropbox/$',views.drop_box_welcome,name= "drop_box_welcome"),
                       url(r'^dropbox/auth/$',views.auth,name= "auth"),
                       url(r'^dropbox/finish/$',views.finish,name= "finish"),)
