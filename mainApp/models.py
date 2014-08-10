import json
import urllib
import urllib2

from django.contrib.auth.models import User
from django.db import models





# Create your models here.


# class UserProfile(User):
#     userSocialId = models.CharField(max_length=200)
#     mobileNumber = models.IntegerField(max_length=20, null=True)
#     accessToken = models.CharField(max_length=300)
#     creationDate = models.DateTimeField(auto_now_add=True)
#     fullName = models.CharField(max_length=300)
#     serviceType = models.TextField(default='FACEBOOK')
#
#
#     def getLatestStreamFacebook(self):
#         fields = "posts.limit(5).fields(description,created_time,name,actions,status_type,message,story)"
#         postsUrl = "https://graph.facebook.com/v2.0/me?access_token=" + self.accessToken + "&fields=" + fields
#         result = urllib2.urlopen(postsUrl)
#         posts = json.load(result)
#         return posts['posts']['data']


class MainUser(models.Model):
    user = models.OneToOneField(User, related_name='mainUser')
    mobile = models.CharField(max_length=10)


class UserSocialProfile(models.Model):
    user = models.ForeignKey(User)
    userSocialId = models.CharField(max_length=200)
    accessToken = models.CharField(max_length=300)
    creationDate = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=300)
    firstName = models.CharField(max_length=300)
    lastName = models.CharField(max_length=300)
    emailAddress = models.CharField(max_length=300)
    serviceType = models.TextField(default='FACEBOOK')

    def getLatestStreamFacebook(self):
        fields = "posts.limit(5).fields(description,created_time,name,actions,status_type,message,story)"
        postsUrl = "https://graph.facebook.com/v2.0/me?access_token=" + self.accessToken + "&fields=" + fields
        result = urllib2.urlopen(postsUrl)
        posts = json.load(result)
        return posts['posts']['data']




def postStatusToFaceBook(accessToken, messageText):
    url = 'https://graph.facebook.com/v2.0/me/feed?access_token=' + accessToken
    data = urllib.urlencode({'message': messageText})
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    status = json.load(response)
    if status.get('id'):
        return True
    else:
        return False
















