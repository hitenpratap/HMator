from django.conf.urls import url
from mainApp import views

urlpatterns = [url(r'^$', views.index, name='index'),
               url(r'^connectToFacebook/$', views.connectToFacebook, name='connectToFacebook'),
               url(r'^getFacebookInfo/$', views.getFacebookInfo, name='getFacebookInfo'),
               url(r'^postStatus.html/$', views.postStatus, name='postStatus'),
               url(r'^facebook/$', views.saveFacebookSettings, name='saveFacebook')
               ]