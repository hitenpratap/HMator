import json
import urllib
import urllib2

from django.contrib.auth.models import User
from django.db import models





# Create your models here.

from twython import Twython

class SocialMessage(models.Model):
    user = models.ForeignKey(User)
    messageTime = models.DateTimeField()
    messageContent = models.TextField()


class MainUser(models.Model):
    user = models.OneToOneField(User, related_name='mainUser')
    mobile = models.CharField(max_length=10)


class UserSocialProfile(models.Model):
    user = models.ForeignKey(User)
    userSocialId = models.CharField(max_length=200)
    accessToken = models.CharField(max_length=300)
    accessTokenSecret = models.CharField(max_length=300,null=True,blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=300)
    firstName = models.CharField(max_length=300,null=True,blank=True)
    lastName = models.CharField(max_length=300,null=True,blank=True)
    emailAddress = models.CharField(max_length=300,null=True,blank=True)
    serviceType = models.TextField(default='FACEBOOK')

    def getLatestStreamFacebook(self):
        fields = "posts.limit(5).fields(description,created_time,name,actions,status_type,message,story)"
        postsUrl = "https://graph.facebook.com/v2.0/me?access_token=" + self.accessToken + "&fields=" + fields
        result = urllib2.urlopen(postsUrl)
        posts = json.load(result)
        return posts['posts']['data']

    def getLatestStreamTwitter(self):
        appId = "APTPUD7sMzwe93QJMBkdoWylw"
        appSecret = "O4iNXzuUWaXITkmmpDQLDmOAWz8tsDAQdh5pbTy7W7exFWyjl0"
        twitter = Twython(appId,appSecret,self.accessToken,self.accessTokenSecret)
        return twitter.get_home_timeline(count=5)




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

def postStatusToTwitter(accessToken,accessTokenSecret, messageText):
    appId = "APTPUD7sMzwe93QJMBkdoWylw"
    appSecret = "O4iNXzuUWaXITkmmpDQLDmOAWz8tsDAQdh5pbTy7W7exFWyjl0"
    twitter = Twython(appId,appSecret,accessToken,accessTokenSecret)
    status = twitter.update_status(status=messageText)
    if status['id']:
        return True
    else:
        return False

















