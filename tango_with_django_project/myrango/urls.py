from django.conf.urls import patterns, url
from myrango import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^log_out/$', views.log_out, name='log_out'),) 