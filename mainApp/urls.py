from django.conf.urls import url

from mainApp import views


urlpatterns = [url(r'^$', views.registration, name='registration'),
               url(r'^streamPage/connectToFacebook/$', views.connectToFacebook, name='connectToFacebook'),
               url(r'^streamPage/connectToTwitter/$', views.connectToTwitter),
               url(r'^connectToTwitter/$', views.connectToTwitter, name='connectToTwitter'),
               url(r'^getFacebookInfo/$', views.getFacebookInfo, name='getFacebookInfo'),
               url(r'^streamPage/postStatus/$', views.postStatus, name='postStatus'),
               url(r'^facebook/$', views.saveFacebookSettings, name='saveFacebook'),
               url(r'^saveTwitterSettings/$', views.saveTwitterSettings, name='saveTwitterSettings'),
               url(r'^autoMaticPostStatus/$', views.autoMaticPostStatus, name='autoMaticPostStatus'),
               url(r'^saveSocialMessages/$', views.saveSocialMessages, name='saveSocialMessages'),
               url(r'^deleteAllSocialMessage/$', views.deleteAllSocialMessage, name='deleteAllSocialMessage'),
               url(r'^updateUserSettings/$', views.updateUserSettings, name='updateUserSettings'),
               url(r'^twitter/$', views.connectToTwitter, name='connectToTwitter'),
               url(r'^getTwitterInfo/$', views.getTwitterInfo, name='getTwitterInfo'),
               url(r'^signup/$', views.signUpUser, name='signUpUser'),
               url(r'^signin/$', views.signInUser, name='signInUser'),
               url(r'^settingsPage/$', views.settingsPage, name='settingsPage'),
               url(r'^streamPage/$', views.streamPage, name='streamPage'),
               url(r'^streamPage/logout/$', views.signOut, name='signOut')

]