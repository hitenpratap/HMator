import json
import urllib2

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect




# Create your views here.
from mainApp.models import postStatusToFaceBook, MainUser, UserSocialProfile


def registration(request):
    print(request.user)
    return render(request, 'mainApp/registration.html')


def signUpUser(request):
    userPass = request.POST['password']
    userMail = request.POST['email']
    userName = userMail
    if userName and userPass and userMail:
        user = User.objects.create_user(username=userName,email=userMail,password=userPass)
        user.first_name = request.POST['firstName']
        user.last_name = request.POST['lastName']
        user.save()
        mainUser = MainUser(mobile = request.POST['mobile'],user=user)
        mainUser.save()
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
                login(request,user)
                print("User is valid, active and authenticated")
                messages.add_message(request, messages.SUCCESS, 'Welcome! '+userMail)
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
    if request.user.is_authenticated():
        try:
            fbSettings = UserSocialProfile.objects.get(user=request.user)
            fbPosts = fbSettings.getLatestStreamFacebook()
            if request.session.get('statusPost'):
                if request.session.get('fbStatus') == 'posted':
                    messages.add_message(request, messages.SUCCESS, 'Post successFully posted to Facebook.')
                else:
                    messages.add_message(request, messages.WARNING, 'Post failed post at Facebook.')
            request.session['statusPost'] = None
            request.session['fbStatus'] = None
            context = {'fbSettings': fbSettings,'fbPosts':fbPosts}
            return render(request, 'mainApp/streams.html', context)
        except UserSocialProfile.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Facebook account is not connected.')
            return render(request, 'mainApp/streams.html')
    else:
        messages.add_message(request, messages.WARNING, 'Please login before continue.')
        return redirect("/HMator/")



def connectToFacebook(request):
    appId = "308183336030888"
    scope = "user_about_me,publish_actions,read_stream"
    redirectUrl = "http://127.0.0.1:8000/HMator/facebook"
    fbUrl = "http://graph.facebook.com/oauth/authorize?client_id=" + appId + "&redirect_uri=" + redirectUrl + "&scope=" + scope

    return HttpResponseRedirect(fbUrl)


def saveFacebookSettings(request):
    redirectUrl = "http://127.0.0.1:8000/HMator/facebook"
    appId = "308183336030888"
    appSecret = "0830a39d4b3c3a1660b26f1db7cf6933"
    code = request.GET['code']
    facebookAccessTokenUrl = "https://graph.facebook.com/oauth/access_token?client_id=" + appId + "&redirect_uri=" + redirectUrl + "&client_secret=" + appSecret + "&code=" + code
    fbResponse = urllib2.urlopen(facebookAccessTokenUrl).read()
    accessToken = ((fbResponse.split("="))[1]).split("&")[0]
    request.session['accessToken'] = accessToken
    print(request.session.get('accessToken'))

    return redirect("/HMator/getFacebookInfo")


def getFacebookInfo(request):
    if request.session.get('accessToken'):
        user = request.user
        accessToken = request.session.get('accessToken')
        requestedFields = "first_name,last_name,email,name"
        requestUrl = "https://graph.facebook.com/me?fields=" + requestedFields + "&access_token=" + accessToken
        result = urllib2.urlopen(requestUrl)
        content = json.load(result)

        facebookSetting = UserSocialProfile(userSocialId=content['id'], firstName=content['first_name'],
                                      lastName=content['last_name'], accessToken=accessToken, serviceType='FACEBOOK',
                                      emailAddress=content['email'], fullName=content['name'],user=user)
        facebookSetting.save()
        return redirect("/HMator/streamPage")

    else:
        return redirect("/HMator/connectToFacebook")


def postStatus(request):
    statusText = request.POST['status']
    if statusText:
        fbSettings = UserSocialProfile.objects.get(serviceType='FACEBOOK')
        try:
            if postStatusToFaceBook(fbSettings.accessToken, statusText):
                faceBookStatus = 'posted'
                request.session['fbStatus'] = faceBookStatus
            request.session['statusPost'] = True
            return redirect('/HMator/')
        except UserSocialProfile.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Facebook account is not connected.')
            return redirect('/HMator/streamPage')
    else:
        messages.add_message(request, messages.WARNING, 'Incorrect information.Please retry by submit your message again.')
        return redirect('/HMator/streamPage')


def connectToTwitter(request):
    appId = "APTPUD7sMzwe93QJMBkdoWylw"
    scope = "user_about_me,publish_actions,read_stream"
    redirectUrl = "http://127.0.0.1:8000/HMator/facebook"
    fbUrl = "http://graph.facebook.com/oauth/authorize?client_id=" + appId + "&redirect_uri=" + redirectUrl + "&scope=" + scope

    return HttpResponseRedirect(fbUrl)


def saveTwitterSettings(request):
    redirectUrl = "http://127.0.0.1:8000/HMator/twitter"
    appId = "APTPUD7sMzwe93QJMBkdoWylw"
    appSecret = "O4iNXzuUWaXITkmmpDQLDmOAWz8tsDAQdh5pbTy7W7exFWyjl0"
    code = request.GET['code']
    facebookAccessTokenUrl = "https://graph.facebook.com/oauth/access_token?client_id=" + appId + "&redirect_uri=" + redirectUrl + "&client_secret=" + appSecret + "&code=" + code
    fbResponse = urllib2.urlopen(facebookAccessTokenUrl).read()
    accessToken = ((fbResponse.split("="))[1]).split("&")[0]
    request.session['accessToken'] = accessToken
    print(request.session.get('accessToken'))

    return redirect("/HMator/getFacebookInfo")


def getTwitterInfo(request):
    if request.session.get('accessToken'):
        user = User.objects.get(email = request.session.get('userEmail'))
        accessToken = request.session.get('accessToken')
        requestedFields = "first_name,last_name,email,name"
        requestUrl = "https://graph.facebook.com/me?fields=" + requestedFields + "&access_token=" + accessToken
        result = urllib2.urlopen(requestUrl)
        content = json.load(result)

        facebookSetting = UserSocialProfile(userSocialId=content['id'], firstName=content['first_name'],
                                      lastName=content['last_name'], accessToken=accessToken, serviceType='FACEBOOK',
                                      emailAddress=content['email'], fullName=content['name'],user=user)
        facebookSetting.save()

    else:
        return redirect("/HMator/connectToFacebook")







