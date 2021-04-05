from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import tweepy
from django.contrib.auth import logout
from .models import User

from django.urls import reverse

from .helpers import get_twitter_api_obj
from django.conf import settings


def home(request):
    return render(request, 'twitter-auth/login.html', {})


def login(request):
    oauth = tweepy.OAuthHandler(settings.API_KEY, settings.API_SECRET)
    auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)
    request.session['request_token'] = oauth.request_token
    return response


def call_back(request):
    auth_verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(settings.API_KEY, settings.API_SECRET)
    token = request.session.get('request_token')
    request.session.delete('request_token')
    oauth.request_token = token
    try:
        oauth.get_access_token(auth_verifier)
    except tweepy.TweepError:
        return HttpResponse("Failed to obtain access token")

    request.session['access_key_tw'] = oauth.access_token
    request.session['access_secret_tw'] = oauth.access_token_secret
    User.objects.get_or_create(
        access_secret=oauth.access_token,
        access_token=oauth.access_token_secret,
    )
    response = HttpResponseRedirect(reverse('profile'))
    return response


def user_profile(request):
    access_token = request.session.get('access_key_tw', None)
    if not access_token:
        return HttpResponseRedirect(reverse('home-view'))
    else:
        obj = get_twitter_api_obj(request)
        current_user = obj.me()
        return render(request, 'twitter-auth/profile.html', {
            'current_user': current_user
        })


def logout_user(request):
    access_token = request.session.get('access_key_tw', None)
    if not access_token:
        request.session.clear()
        logout(request)
    return HttpResponseRedirect(reverse('home-view'))

