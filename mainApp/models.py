import json
import urllib
import urllib2

from django.db import models



# Create your models here.


class User(models.Model):
    userSocialId = models.CharField(max_length=200)
    firstName = models.CharField(max_length=300)
    lastName = models.CharField(max_length=300)
    emailAddress = models.EmailField(max_length=300)
    mobileNumber = models.IntegerField(max_length=20, null=True)
    accessToken = models.CharField(max_length=300)
    creationDate = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=300)
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
















