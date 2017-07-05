from rest_framework import serializers, views
from .serializers import LSTMSerializer
from rest_framework.response import Response
from .lstm_model import runLSTM
import tweepy
import unicodedata
from .models import LSTM

# Consumer keys and access tokens, used for OAuth - Twitter
CONSUMER_KEY = 'DIxitlH7HaqT0SxvHXZ0cDuEP'
CONSUMER_SECRET = 'WmuPQykTvYsuHvVuRmGqJ9PSIp8MkpLd1rWWigJ84zv2Yq4r1o'
ACCESS_TOKEN = '159242496-v2B8e5ALI0Ois5pg0XP6fOM4JoszrzIeE8SLgOZC'
ACCESS_TOKEN_SECRET = 'nuZkXJxjyxB5cOuEoeqylaakAa1lhyn4Pf33INdpB8h9R'

'''
Some results from request/responses
curl 127.0.0.1:8000/modelapi/?model_input="I hate these new features On ThisPhone after the update."
{
    "movies": {
        "movie_2": {
            "overview": "The cunning and wicked Urfin wants to become ruler of Magic Land. With an army of wooden soldiers, he captures the Emerald City and renames it ti Urfinville. He is all but ready to celebrate victory, when his plans are ruined by an ordinary girl named Dorothy, who arrives in Magic Land just at the right time. She must return home, but not before she helps her friends - the Scarecrow, the Tin Man, and new-brave Lion - defeat Urfin. And in order to do that, they need to find out who he really is.",
            "tmdb_link": "https://www.themoviedb.org/movie/441957",
            "poster_path": "https://image.tmdb.org/t/p/w640/fYG0IvEdQ54KM7r6IQ0ETrGj4Il.jpg",
            "id": 441957,
            "title": "Fantastic Journey to Oz"
        },
        "movie_3": {
            "overview": "In 2013, something terrible is awakening in London's National Gallery; in 1562, a murderous plot is afoot in Elizabethan England; and somewhere in space an ancient battle reaches its devastating conclusion. All of reality is at stake as the Doctor's own dangerous past comes back to haunt him.",
            "tmdb_link": "https://www.themoviedb.org/movie/313106",
            "poster_path": "https://image.tmdb.org/t/p/w640/lQy2QVcacuH55k37K9Ox0gw3YpZ.jpg",
            "id": 313106,
            "title": "Doctor Who: The Day of the Doctor"
        },
        "movie_1": {
            "overview": "Interstellar chronicles the adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.",
            "tmdb_link": "https://www.themoviedb.org/movie/157336",
            "poster_path": "https://image.tmdb.org/t/p/w640/nBNZadXqJSdt05SHLqgT0HuC5Gm.jpg",
            "id": 157336,
            "title": "Interstellar"
        }
    },
    "options": {
        "end_year": 2017,
        "start_year": 2012,
        "rating": 8.0
    },
    "feelings": {
        "anger": 64.23,
        "joy": 1.02,
        "fear": 4.88,
        "sadness": 22.71,
        "disgust": 7.16
    }
}
'''


class LSTMView(views.APIView):
    def get(self, request):
        '''
        WARNING:
        We must not use hashtags in the input text to the API.
        '''
        serializer = LSTMSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        model_input = data["model_input"]

        # If model_input was a username @magedmagdy01
        # We will use this to solve authentications problems in Moviefy mobile app
        # The mobile app will send an API request to get movies recommendation and feelings of the user
        # and provides the username, we will do the rest, grab the user tweets, run the model on them, and output the results in json response.
        model_input = unicodedata.normalize('NFKD', model_input).encode('ascii', 'ignore')
        # model_input = "@magedmagdy01"

        model_input = model_input[1:-1]
        # model_input = @magedmagdy01

        if model_input.startswith('@'):
            # @username
            # OAuth process, using the keys and tokens
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            # Creation of the actual interface, using authentication
            api = tweepy.API(auth)
            # Getting the recent user tweets
            timeline = api.user_timeline(screen_name=model_input, count=10, include_rts=False)
            user_tweets = []
            for status in timeline:
                if status.lang == "en":
                    user_tweets.append(status.text)

            # Check if user_tweets is empty .. i.e. we didn't find any english tweets to process on
            # We will return an error response in this case
            if not user_tweets:
                return Response({
                    "error_code": 500,
                    "error_message": "Sorry, we are unable to process your tweets. Please check if you already have your Tweets written on English as currently our algorithm only runs on English text only."
                })
            else:
                # Converting the list of tweets to a full string separated by "\r\n"
                model_input = "\r\n".join(user_tweets)

        else:
            return Response({
                "error_code": 400,
                "error_message": "Invalid input, username must start with @"
            })

        # Default values if not provided by the user of the API
        startYear = 2010
        endYear = 2017
        movieRating = 7

        # Get the user defined options if any is provided
        try:
            startYear = data["start_year"]
        except:
            pass
        try:
            endYear = data["end_year"]
        except:
            pass
        try:
            movieRating = data["rating"]
        except:
            pass

        '''
        Saving to the database
        '''
        LSTM_instance = LSTM.objects.create(model_input=model_input, start_year=startYear, end_year=endYear, rating=movieRating)

        # movie_year = data["movie_year"]
        # rating = data["rating"]
        '''
        Shape of data: data = [feelings, movies_json]
        feelings = data[0]
        movies_json = data[1]
        '''
        data = runLSTM(str(model_input), rating=movieRating, startYear=startYear, endYear=endYear)
        feelings = data[0]
        # returns a list of 3 movies selected based on the input criteria
        movies_json = data[1]

        # result = "Happy, 70%, Terminal"

        return Response({
            "feelings": {
                "anger": feelings[0],
                "disgust": feelings[1],
                "fear": feelings[2],
                "joy": feelings[3],
                "sadness": feelings[4],
            },
            "movies": {
                "movie_1": {
                    "title": movies_json[0]["title"],
                    "overview": movies_json[0]["overview"],
                    "poster_path": "https://image.tmdb.org/t/p/w640" + movies_json[0]["poster_path"],
                    "id": movies_json[0]["id"],
                    "tmdb_link": "https://www.themoviedb.org/movie/" + str(movies_json[0]["id"]),
                    "popularity": movies_json[0]["popularity"],
                },
                "movie_2": {
                    "title": movies_json[1]["title"],
                    "overview": movies_json[1]["overview"],
                    "poster_path": "https://image.tmdb.org/t/p/w640" + movies_json[1]["poster_path"],
                    "id": movies_json[1]["id"],
                    "tmdb_link": "https://www.themoviedb.org/movie/" + str(movies_json[1]["id"]),
                    "popularity": movies_json[1]["popularity"],

                },
                "movie_3": {
                    "title": movies_json[2]["title"],
                    "overview": movies_json[2]["overview"],
                    "poster_path": "https://image.tmdb.org/t/p/w640" + movies_json[2]["poster_path"],
                    "id": movies_json[2]["id"],
                    "tmdb_link": "https://www.themoviedb.org/movie/" + str(movies_json[2]["id"]),
                    "popularity": movies_json[2]["popularity"],
                },

            },
            "options": {
                "start_year": startYear,
                "end_year": endYear,
                "rating": movieRating,
            }

        })
