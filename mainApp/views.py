from datetime import datetime, timedelta
import json
import urllib2

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response





# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import tweetpony
from twython import Twython
from mainApp.models import postStatusToFaceBook, MainUser, UserSocialProfile, postStatusToTwitter, SocialMessage


def registration(request):
    print(request.user)
    return render(request, 'mainApp/registration.html')


def signUpUser(request):
    userPass = request.POST['password']
    userMail = request.POST['email']
    userName = userMail
    if userName and userPass and userMail:
        user = User.objects.create_user(username=userName, email=userMail, password=userPass)
        user.first_name = request.POST['firstName']
        user.last_name = request.POST['lastName']
        user.save()
        mainUser = MainUser(mobile=request.POST['mobile'], user=user)
        mainUser.save()
        user = authenticate(username=userMail, password=userPass)
        login(request, user)
        return redirect("/HMator/streamPage")
    else:
        messages.add_message(request, messages.WARNING, 'Incorrect Information. Please try again.')
        return render(request, 'mainApp/registration.html', {'viewPage': 'signupbox'})
        # request was empty


def signInUser(request):
    userMail = request.POST['email']
    userPass = request.POST['password']
    logout(request)
    if userMail and userPass:
        user = authenticate(username=userMail, password=userPass)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print(user)
                login(request, user)
                print("User is valid, active and authenticated")
                messages.add_message(request, messages.SUCCESS, 'Welcome! ' + userMail)
                return redirect('/HMator/streamPage')
            else:
                messages.add_message(request, messages.WARNING,
                                     'The password is valid, but the account has been disabled!')
                return render(request, 'mainApp/registration.html', {'viewPage': 'loginbox'})
        else:
            # the authentication system was unable to verify the username and password
            messages.add_message(request, messages.WARNING, 'Username or Password is wrong. Please try again.')
            return render(request, 'mainApp/registration.html', {'viewPage': 'loginbox'})
    else:
        messages.add_message(request, messages.WARNING, 'Incorrect information. Please try again.')
        return render(request, 'mainApp/registration.html', {'viewPage': 'loginbox'})


def signOut(request):
    logout(request)
    return redirect("/HMator/")


def streamPage(request):
    print(datetime.now().time())
    request.session['currentUserId']=request.user.id
    if request.user.is_authenticated():
        try:
            user = request.user
            fbSettings = UserSocialProfile.objects.get(serviceType='FACEBOOK', user=user)
            twitterSettings = UserSocialProfile.objects.get(serviceType='TWITTER', user=user)
            fbPosts = fbSettings.getLatestStreamFacebook()
            twitterPosts = twitterSettings.getLatestStreamTwitter()
            if request.session.get('statusPost'):
                if request.session.get('fbStatus') == 'posted':
                    messages.add_message(request, messages.SUCCESS, 'Post successFully posted to Facebook.')
                if request.session.get('twitterStatus') == 'posted':
                    messages.add_message(request, messages.SUCCESS, 'Post successFully posted to Twitter.')
                else:
                    messages.add_message(request, messages.WARNING, 'Post failed post at Facebook.')
            request.session['statusPost'] = None
            request.session['fbStatus'] = None
            request.session['twitterStatus'] = None
            context = {'fbSettings': fbSettings, 'fbPosts': fbPosts, 'twitterSettings': twitterSettings,
                       'twitterPosts': twitterPosts}
            return render(request, 'mainApp/streams.html', context)
        except UserSocialProfile.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Facebook account is not connected.')
            return render(request, 'mainApp/streams.html')
    else:
        messages.add_message(request, messages.WARNING, 'Please login before continue.')
        return redirect("/HMator/")


def connectToFacebook(request):
    appId = "Use your api key"
    scope = "user_about_me,publish_actions,read_stream"
    redirectUrl = "http://127.0.0.1:8000/HMator/facebook"
    fbUrl = "http://graph.facebook.com/oauth/authorize?client_id=" + appId + "&redirect_uri=" + redirectUrl + "&scope=" + scope

    return HttpResponseRedirect(fbUrl)


def saveFacebookSettings(request):
    redirectUrl = "http://127.0.0.1:8000/HMator/facebook"
    appId = "Use your api key"
    appSecret = "Use your api key"
    code = request.GET['code']
    facebookAccessTokenUrl = "https://graph.facebook.com/oauth/access_token?client_id=" + appId + "&redirect_uri=" + redirectUrl + "&client_secret=" + appSecret + "&code=" + code
    fbResponse = urllib2.urlopen(facebookAccessTokenUrl).read()
    accessToken = ((fbResponse.split("="))[1]).split("&")[0]
    request.session['accessToken'] = accessToken
    print(request.session.get('accessToken'))

    return redirect("/HMator/getFacebookInfo")


def getFacebookInfo(request):
    if request.session.get('accessToken'):
        user = MainUser.objects.get(user=request.user)
        accessToken = request.session.get('accessToken')
        requestedFields = "first_name,last_name,email,name"
        requestUrl = "https://graph.facebook.com/me?fields=" + requestedFields + "&access_token=" + accessToken
        result = urllib2.urlopen(requestUrl)
        content = json.load(result)

        facebookSetting = UserSocialProfile(userSocialId=content['id'], firstName=content['first_name'],
                                            lastName=content['last_name'], accessToken=accessToken,
                                            serviceType='FACEBOOK',
                                            emailAddress=content['email'], fullName=content['name'], user=user)
        facebookSetting.save()
        return redirect("/HMator/streamPage")

    else:
        return redirect("/HMator/connectToFacebook")
@csrf_exempt
def autoMaticPostStatus(request):
    print(request.POST)
    print(request.session.get('currentUserId'))
    user = User.objects.get(id=1)
    mainUser = MainUser.objects.get(user=user)
    print("-------------------------------------------------------------------")
    twitterSettings = UserSocialProfile.objects.get(user=mainUser,serviceType='TWITTER')
    fbSettings = UserSocialProfile.objects.get(user=mainUser,serviceType='FACEBOOK')

    messageList = SocialMessage.objects.filter(user=mainUser)
    currentTime = datetime.now().time()
    print(currentTime)
    print(messageList)
    for msg in messageList:
        print(msg.messageContent)
        if currentTime.hour==msg.messageTime.hour:
            print("***********************************************************************")
            print(msg.messageContent)
            # if fbSettings is not None:
                # postStatusToFaceBook(fbSettings.accessToken,msg.messageContent)
            # if twitterSettings is not None:
            #     postStatusToTwitter(twitterSettings.accessToken,twitterSettings.accessTokenSecret,msg.messageContent)

    # return 'Post Messages'





def postStatus(request):
    statusText = request.POST['status']
    if statusText:
        try:
            if request.POST.get('facebook'):
                fbSettings = UserSocialProfile.objects.get(serviceType='FACEBOOK', user=request.user)
                if fbSettings and postStatusToFaceBook(fbSettings.accessToken, statusText):
                    request.session['fbStatus'] = 'posted'
            if request.POST.get('twitter'):
                twitterSettings = UserSocialProfile.objects.get(serviceType='TWITTER', user=request.user)
                if twitterSettings and postStatusToTwitter(twitterSettings.accessToken,
                                                           twitterSettings.accessTokenSecret, statusText):
                    request.session['twitterStatus'] = 'posted'
                request.session['statusPost'] = True
                return redirect('/HMator/streamPage')
        except UserSocialProfile.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Facebook account is not connected.')
            return redirect('/HMator/streamPage')
    else:
        messages.add_message(request, messages.WARNING,
                             'Incorrect information.Please retry by submit your message again.')
        return redirect('/HMator/streamPage')


def connectToTwitter(request):
    appId = "Use your api key"
    appSecret = "Use your api key"
    twitter = Twython(appId, appSecret)
    auth = twitter.get_authentication_tokens(callback_url='http://127.0.0.1:8000/HMator/saveTwitterSettings/')
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    print(OAUTH_TOKEN)
    print(OAUTH_TOKEN_SECRET)
    request.session['OAUTH_TOKEN'] = OAUTH_TOKEN
    request.session['OAUTH_TOKEN_SECRET'] = OAUTH_TOKEN_SECRET
    return redirect(auth['auth_url'])


def saveTwitterSettings(request):
    if request.session.get('OAUTH_TOKEN_SECRET') and request.session.get('OAUTH_TOKEN'):
        user = request.user
        appId = "Use your api key"
        appSecret = "Use your api key"
        OAUTH_TOKEN = request.session.get('OAUTH_TOKEN')
        OAUTH_TOKEN_SECRET = request.session.get('OAUTH_TOKEN_SECRET')
        oauth_verifier = request.GET['oauth_verifier']
        twitter = Twython(appId, appSecret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        final_step = twitter.get_authorized_tokens(oauth_verifier)
        FOAUTH_TOKEN = final_step['oauth_token']
        FOAUTH_TOKEN_SECERT = final_step['oauth_token_secret']
        request.session['FOAUTH_TOKEN'] = FOAUTH_TOKEN
        request.session['FOAUTH_TOKEN_SECERT'] = FOAUTH_TOKEN_SECERT
        return redirect("/HMator/getTwitterInfo")
    else:
        return redirect("/HMator/connectToTwitter")


def getTwitterInfo(request):
    if request.session.get('FOAUTH_TOKEN') and request.session.get('FOAUTH_TOKEN_SECERT'):
        user = MainUser.objects.get(user=request.user)
        accessToken = request.session.get('FOAUTH_TOKEN')
        accessTokenSecret = request.session.get('FOAUTH_TOKEN_SECERT')
        appId = "Use your api key"
        appSecret = "Use your api key"
        twitter = Twython(appId, appSecret, accessToken, accessTokenSecret)
        content = twitter.verify_credentials()
        print(content['id'])
        twitterSettings = UserSocialProfile(userSocialId=content['id'], accessToken=accessToken,
                                            accessTokenSecret=accessTokenSecret,
                                            serviceType='TWITTER', fullName=content['name'], user=user)
        print(content['name'])
        twitterSettings.save()
        return redirect("/HMator/streamPage")
    else:
        return redirect("/HMator/saveTwitterSettings")


def settingsPage(request):
    if request.user.is_authenticated():
        mainUser = MainUser.objects.get(user=request.user)
        userSocialProfileList = UserSocialProfile.objects.filter(user=mainUser)
        accountList = []
        for userSocialProfile in userSocialProfileList:
            accountList.append(userSocialProfile.serviceType)
        socialMessages = SocialMessage.objects.filter(user=mainUser)
        return render(request, 'mainApp/settings.html', {'user': request.user, 'accountList': accountList,'socialMessages':socialMessages})
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login to continue.')
        return redirect('/HMator/')


def updateUserSettings(request):
    mainUser = MainUser.objects.get(id=request.POST['userId'])
    if mainUser:
        print(request.POST['firstName'])
        mainUser.user.first_name = request.POST['firstName']
        mainUser.user.last_name = request.POST['lastName']
        mainUser.mobile = request.POST['phoneNumber']
        mainUser.user.save(force_update=True)
        mainUser.save(force_update=True)
        messages.add_message(request, messages.INFO,
                             'User settings updated successfully.')
        return redirect("/HMator/settingsPage")
    else:
        messages.add_message(request, messages.WARNING,
                             'Something went wrong. Please try again.')
        return redirect("/HMator/settingsPage")

def saveSocialMessages(request):
    mainUser = MainUser.objects.get(user=request.user)
    messageTextList = request.POST.getlist('messageText')
    messageHourList = request.POST.getlist('messageHour')
    messageMinList = request.POST.getlist('messageMin')

    existMessages = SocialMessage.objects.filter(user=mainUser)
    for msg in existMessages:
        msg.delete()

    for idx,messageText in enumerate(messageTextList):
        if messageHourList[idx]!='' and messageText!='':
            socialMessage = SocialMessage(user=mainUser,messageContent=messageText,messageTime=datetime.now().replace(hour=int(messageHourList[idx]),minute=int(messageMinList[idx])).time())
            socialMessage.save()

    messages.add_message(request, messages.INFO,
                             'Messages saved successfully.')
    return redirect("/HMator/settingsPage")


def deleteAllSocialMessage(request):
    user = MainUser.objects.get(user = request.user)
    existMessages = SocialMessage.objects.filter(user=user)
    for msg in existMessages:
        msg.delete()
    return render_to_response('mainApp/socialMessageList.html')












