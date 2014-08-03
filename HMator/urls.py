from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^HMator/', include('mainApp.urls',namespace='mailApp')),
    url(r'^admin/', include(admin.site.urls)),
]
