import uuid

from mainApp.models import UserSocialProfile, postStatusToTwitter


def my_scheduled_job():
    twitterSettings = UserSocialProfile.objects.get(serviceType='TWITTER')
    print(str(uuid.uuid1()))
    postStatusToTwitter(twitterSettings.accessToken, twitterSettings.accessTokenSecret, str(uuid.uuid1()))







