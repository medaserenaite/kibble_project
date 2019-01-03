from django.conf.urls import url
from . import views
 
urlpatterns = [

    url(r'^$', views.index),
    url(r'^admin$', views.admin),
    url(r'^admin_dashboard$', views.admin_dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_appt$', views.add_appt),
    url(r'^edit/(?P<id>\d+)/$',views.edit),
    url(r'^update/(?P<id>\d+)/$',views.update),
    url(r'^destroy/(?P<id>\d+)/$',views.destroy),
    url(r'^approve/(?P<id>\d+)/$',views.approve)
 ]