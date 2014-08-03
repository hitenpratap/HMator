import json
import urllib
import urllib2
from django.contrib import messages
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.
from mainApp.models import User, postStatusToFaceBook


def index(request):
    fbSettings = User.objects.get(serviceType='FACEBOOK')
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

    return HttpResponseRedirect("http://127.0.0.1:8000/HMator/getFacebookInfo")


def getFacebookInfo(request):
    if request.session.get('accessToken'):
        accessToken = request.session.get('accessToken')
        requestedFields = "first_name,last_name,email,name"
        requestUrl = "https://graph.facebook.com/me?fields=" + requestedFields + "&access_token=" + accessToken
        result = urllib2.urlopen(requestUrl)
        content = json.load(result)

        facebookSetting = User(userSocialId=content['id'], firstName=content['first_name'],
                               lastName=content['last_name'], accessToken=accessToken, serviceType='FACEBOOK',
                               emailAddress=content['email'], fullName=content['name'])
        facebookSetting.save()

    else:
        return HttpResponseRedirect("http://127.0.0.1:8000/HMator/connectToFacebook")

def postStatus(request):
    statusText = request.POST['status']
    fbSettings = User.objects.get(serviceType='FACEBOOK')
    if postStatusToFaceBook(fbSettings.accessToken,statusText):
        faceBookStatus = 'posted'
        request.session['fbStatus'] = faceBookStatus
    request.session['statusPost'] = True
    return redirect('http://127.0.0.1:8000/HMator/')







