import urllib, urllib3
import requests
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse

from profiles.models import Configuration

INSTAGRAM_CLIENT_ID = getattr(settings, "INSTAGRAM_CLIENT_ID", None)
INSTAGRAM_CLIENT_SECRET = getattr(settings, 'INSTAGRAM_CLIENT_SECRET', None)
INSTAGRAM_REDIRECT_URI = getattr(settings, "INSTAGRAM_REDIRECT_URI", None)

def home_page_view(request):
    context = {
        "INSTAGRAM_CLIENT_ID": INSTAGRAM_CLIENT_ID,
        "INSTAGRAM_REDIRECT_URI": INSTAGRAM_REDIRECT_URI
    }
    return render(request, 'home_page.html', context)

def response_view(request):
    instagram_user_code = request.GET.get("code", None)
    if instagram_user_code is None:
        return HttpResponse("Something went wrong")
    else:
        url = 'https://api.instagram.com/oauth/access_token'
        values = {
            'client_id': INSTAGRAM_CLIENT_ID,
            'client_secret': INSTAGRAM_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': INSTAGRAM_REDIRECT_URI,
            'code': instagram_user_code,
        }
        req = requests.post(url, values)
        response = req.text
        jData = json.loads(response)
        if 'access_token' in jData and 'user' in jData:
            configuration_obj = Configuration.objects.create(ad_pk='hey3')
            configuration_obj.access_token = jData['access_token']
            configuration_obj.save()
            print('success')
        elif request.GET.get('error'):
            return HttpResponse('Error')
        return redirect('home')

def response_access_token_view(request):
    return render(request, 'access_token.html', {})

def response2(request):
    if 'code' in request.GET:
        url = 'https://api.instagram.com/oauth/access_token'
        values = {
            'client_id': 'fbcc55f279754d9f9779f61030548ddc',
            'client_secret':'783b711f9ed645f9b5e1d38a546fcf52',
            'redirect_uri':'http://localhost:8000/response/',
            'code':request.GET.get('code'),
            'grant_type':'authorization_code'
        }
        req = requests
        data = urllib.parse.urlencode(values).encode("utf-8")
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        response_string = response.read()
        insta_data = json.loads(response_string)
        if 'access_token' in insta_data and 'user' in insta_data:
            #authentication success
            print(insta_data['access_token'])
            return redirect('ads:new')
        else:
            #authentication failure after step 2
            return HttpResponse("error 2")
    elif 'error' in request.GET:
        #authentication failure after step 1
        return HttpResponse("error 1")
    else:
        return HttpResponse("error 3")