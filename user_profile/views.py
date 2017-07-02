from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic
from allauth.socialaccount.models import SocialToken
import oauth2
import tweepy

# Twitter Consumer Keys for Moviefy 2 App.
CONSUMER_KEY = "DIxitlH7HaqT0SxvHXZ0cDuEP"
CONSUMER_SECRET = "WmuPQykTvYsuHvVuRmGqJ9PSIp8MkpLd1rWWigJ84zv2Yq4r1o"

# Accessing Single User Tweets using OAuth2
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content



def profile(request):
    # Get the access token for the logged in user to retrieve their tweets
    # access_token has 2 values: TOKEN: access_token.token ** SECRET: access_token.token_secret
    access_token = SocialToken.objects.get(account__user=request.user, account__provider='twitter')

    # Accessing user tweets using the access token we that saved from login using allauth
    #user_timeline = oauth_req('https://api.twitter.com/1.1/statuses/user_timeline.json', access_token.token, access_token.token_secret)

    # Using Tweepy for Accessing user tweets using the access token we that saved from login using allauth
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(access_token.token,access_token.token_secret)
    api = tweepy.API(auth)
    timeline = api.user_timeline(screen_name=request.user.username, count=10, include_rts=False)
    # List of retrieved user tweets - Text only - (10 recent tweets)
    user_tweets = []
    for status in timeline:
        user_tweets.append(status.text  )

    context = {
        'user_tweets': user_tweets,
        'access_token': access_token,
    }
    return render(request, "profile.html", context)