import json
import urllib
import urllib2
import uuid
from django.template.defaulttags import csrf_token

from mainApp.models import UserSocialProfile, postStatusToTwitter


def my_scheduled_job():
    twitterSettings = UserSocialProfile.objects.get(serviceType='TWITTER')
    # print(str(uuid.uuid1()))
    # postStatusToTwitter(twitterSettings.accessToken, twitterSettings.accessTokenSecret, 'Good Evening :)')
    url = 'http://127.0.0.1:8000/HMator/autoMaticPostStatus/'
    data = urllib.urlencode({'message': 'Running cron job to post messages','csrfmiddlewaretoken':csrf_token})
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    status = json.load(response)








