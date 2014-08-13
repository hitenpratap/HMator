# @kronos.register('* * * * *')
# def complain():
#     postInfo = {'06:00': 'Good Morning..', '09:00': 'Good Day..', '13:00': 'Good AfterNoon..',
#                 '18:00': 'Good Evening..', '22:00': 'Good Night..'}
#     currentTime = datetime.now().strftime('%H:%M')
#     if currentTime in postInfo.keys():
#         statusText = postInfo.get(currentTime)
#         fbSettings = UserProfile.objects.get(serviceType='FACEBOOK')
#         # postStatusToFaceBook(fbSettings.accessToken,statusText)
#
#     else:
#         statusText = 'Test Message'
#         fbSettings = UserProfile.objects.get(serviceType='FACEBOOK')
#         # postStatusToFaceBook(fbSettings.accessToken,currentTime + statusText)
import uuid

from mainApp.models import UserSocialProfile, postStatusToTwitter


def my_scheduled_job():
    twitterSettings = UserSocialProfile.objects.get(serviceType='TWITTER')
    print(str(uuid.uuid1()))
    postStatusToTwitter(twitterSettings.accessToken, twitterSettings.accessTokenSecret, str(uuid.uuid1()))







