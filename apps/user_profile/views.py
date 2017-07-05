from django.shortcuts import render
from allauth.socialaccount.models import SocialToken
#import oauth2
from rest_framework import views
from .serializers import UserDetailsSerializer
from rest_framework.response import Response
import tweepy
import unicodedata
from .models import UserDetails

# Twitter Consumer Keys for Moviefy 2 App.
CONSUMER_KEY = "DIxitlH7HaqT0SxvHXZ0cDuEP"
CONSUMER_SECRET = "WmuPQykTvYsuHvVuRmGqJ9PSIp8MkpLd1rWWigJ84zv2Yq4r1o"
ACCESS_TOKEN = '159242496-v2B8e5ALI0Ois5pg0XP6fOM4JoszrzIeE8SLgOZC'
ACCESS_TOKEN_SECRET = 'nuZkXJxjyxB5cOuEoeqylaakAa1lhyn4Pf33INdpB8h9R'

'''
NOT USED
# Accessing Single User Tweets using OAuth2
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content
'''

# Return Profile View for each user logged in.
def profile(request):
    if (request.user.is_authenticated):
        # Get the access token for the logged in user to retrieve their tweets
        # access_token has 2 values: TOKEN: access_token.token ** SECRET: access_token.token_secret
        access_token = SocialToken.objects.get(account__user=request.user, account__provider='twitter')

        # Accessing user tweets using the access token we that saved from login using allauth
        # user_timeline = oauth_req('https://api.twitter.com/1.1/statuses/user_timeline.json', access_token.token, access_token.token_secret)

        # Using Tweepy for Accessing user tweets using the access token we that saved from login using allauth
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(access_token.token, access_token.token_secret)
        api = tweepy.API(auth)
        timeline = api.user_timeline(screen_name=request.user.username, count=10, include_rts=False)
        # List of retrieved user tweets - Text only - (10 recent tweets)
        lang = True # True means english
        user_tweets = []
        for status in timeline:
            if status.lang == "en":
                user_tweets.append(status.text)

        if not user_tweets:
            lang = False

        context = {
            'user_tweets': user_tweets,
            'access_token': access_token,
            'lang': lang
        }
    else:
        context = {}

    return render(request, "profile.html", context)



# User API view

class UserProfileView(views.APIView):
    def get(self, request):
        serializer = UserDetailsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        username = data["username"]

        username = unicodedata.normalize('NFKD', username).encode('ascii', 'ignore')
        # username = "@magedmagdy01"

        username = username[1:-1]
        # username = @magedmagdy01

        # username must start with '@'
        if username.startswith('@'):
            # @username
            # OAuth process, using the keys and tokens
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            # Creation of the actual interface, using authentication
            api = tweepy.API(auth)

            # Getting the user timeline
            timeline = api.user_timeline(screen_name=username, count=10, include_rts=False)

            user_tweets = []
            for status in timeline:
                if status.lang == "en":
                    user_tweets.append(status.text)

            # Check if user_tweets is empty .. i.e. we didn't find any english tweets to process on
            # We will return an error response in this case
            if not user_tweets:
                user_tweets = ""
                return Response({
                    "error_code": 500,
                    "error_message": "Sorry, we are unable to process your tweets. Please check if you already have your Tweets written on English as currently our algorithm only runs on English text only."
                })
            else:
                # Converting the list of tweets to a full string separated by "\r\n"
                user_tweets = "\r\n".join(user_tweets)


            # Extracting user avatar
            user_profile = api.get_user(screen_name=username)
            avatar_url = user_profile.profile_image_url_https.replace('_normal', '')

            '''
           Saving to the database
           '''
            UserDetails_instance = UserDetails.objects.create(username=username, avatar_url=avatar_url, user_tweets=user_tweets)

            return Response({
                "avatar_url": avatar_url,
                "user_tweets": user_tweets,
            })

        else:
            return Response({
                "error_code": 400,
                "error_message": "Invalid input, username must start with @"
            })

