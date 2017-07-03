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
