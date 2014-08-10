from django.conf.urls import url

from mainApp import views


urlpatterns = [url(r'^$', views.registration, name='registration'),
               url(r'^streamPage/connectToFacebook/$', views.connectToFacebook, name='connectToFacebook'),
               url(r'^getFacebookInfo/$', views.getFacebookInfo, name='getFacebookInfo'),
               url(r'^streamPage/postStatus/$', views.postStatus, name='postStatus'),
               url(r'^facebook/$', views.saveFacebookSettings, name='saveFacebook'),
               url(r'^signup/$', views.signUpUser, name='signUpUser'),
               url(r'^signin/$', views.signInUser, name='signInUser'),
               url(r'^streamPage/$', views.streamPage, name='streamPage'),
               url(r'^streamPage/logout/$', views.signOut, name='signOut')

]