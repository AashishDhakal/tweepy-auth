import tweepy

from django.conf import settings


def get_twitter_api_obj(request):
    oauth = tweepy.OAuthHandler(settings.API_KEY, settings.API_SECRET)
    access_key = request.session['access_key_tw']
    access_secret = request.session['access_secret_tw']
    oauth.set_access_token(access_key, access_secret)
    api = tweepy.API(oauth)
    return api
