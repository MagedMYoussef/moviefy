from rest_framework import serializers, views
from .serializers import LSTMSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from .lstm_model import runLSTM

'''
Some results from request/responses
curl 127.0.0.1:8000/modelapi/?model_input="I hate these new features On ThisPhone after the update."
{
    "movies": {
        "movie_2": {
            "overview": "This is the extraordinary tale of two brothers named Moses and Ramses, one born of royal blood, and one an orphan with a secret past. Growing up the best of friends, they share a strong bond of free-spirited youth and good-natured rivalry. But the truth will ultimately set them at odds, as one becomes the ruler of the most powerful empire on earth, and the other the chosen leader of his people! Their final confrontation will forever change their lives and the world.",
            "poster_path": "/wD34ls2faCrj8YvFViEaPfBtBEe.jpg",
            "id": 9837,
            "title": "The Prince of Egypt"
        },
        "movie_3": {
            "overview": "A young witch, on her mandatory year of independent life, finds fitting into a new community difficult while she supports herself by running an air courier service.",
            "poster_path": "/d5gLpu8kqyPs27bh9IiCuwMDjDh.jpg",
            "id": 16859,
            "title": "Kiki's Delivery Service"
        },
        "movie_1": {
            "overview": "Tarzan was a small orphan who was raised by an ape named Kala since he was a child. He believed that this was his family, but on an expedition Jane Porter is rescued by Tarzan. He then finds out that he's human. Now Tarzan must make the decision as to which family he should belong to...",
            "poster_path": "/hnTrfKJmnPLMTajHw2RDgv6hVyH.jpg",
            "id": 37135,
            "title": "Tarzan"
        }
    },
    "options": {
        "rating": "rating",
        "movie_year": "movie_year"
    },
    "feelings": {
        "anger": 63.56,
        "joy": 0.95,
        "fear": 5.01,
        "sadness": 23.14,
        "disgust": 7.34
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

        # Default values if not provided by the user of the API
        startYear = 2010
        endYear = 2017
        movieRating = 7
        try:
            start_year = data["start_year"]
        except:
            pass
        # movie_year = data["movie_year"]
        # rating = data["rating"]
        '''
        Shape of data: data = [feelings, movies_json]
        feelings = data[0]
        movies_json = data[1]
        '''
        data = runLSTM(str(model_input), rating=movieRating,startYear=startYear, endYear=endYear)
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
                    "poster_path":"https://image.tmdb.org/t/p/w640" + movies_json[0]["poster_path"],
                    "id":movies_json[0]["id"],
                    "tmdb_link": "https://www.themoviedb.org/movie/" + str(movies_json[0]["id"]),
                },
                "movie_2": {
                    "title": movies_json[1]["title"],
                    "overview": movies_json[1]["overview"],
                    "poster_path": "https://image.tmdb.org/t/p/w640" + movies_json[1]["poster_path"],
                    "id": movies_json[1]["id"],
                    "tmdb_link": "https://www.themoviedb.org/movie/" + str(movies_json[1]["id"]),
                },
                "movie_3": {
                    "title": movies_json[2]["title"],
                    "overview": movies_json[2]["overview"],
                    "poster_path": "https://image.tmdb.org/t/p/w640" + movies_json[2]["poster_path"],
                    "id": movies_json[2]["id"],
                    "tmdb_link": "https://www.themoviedb.org/movie/" + str(movies_json[2]["id"]),

                },

            },
            "options": {
                "start_year": startYear,
                "end_year": endYear,
                "rating": movieRating,
            }

        })
