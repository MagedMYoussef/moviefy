from rest_framework import serializers, views
from .serializers import LSTMSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from .lstm_model import runLSTM

'''
Some results from request/responses
curl 127.0.0.1:8000/modelapi/?model_input="I am very happy today"
{
    "movies": {
        "movie_2": "NOT YET",
        "movie_3": "NOT YET",
        "movie_1": "NOT YET"
    },
    "options": {
        "rating": "rating",
        "movie_year": "movie_year"
    },
    "feelings": {
        "anger": 0.006648946087807417,
        "joy": 0.9444617033004761,
        "fear": 0.010349957272410393,
        "sadness": 0.036381904035806656,
        "disgust": 0.0021575307473540306
    }
}
'''
class LSTMView(views.APIView):

    def get(self, request):
        serializer = LSTMSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        model_input = data["model_input"]
        #movie_year = data["movie_year"]
        #rating = data["rating"]
        feelings = runLSTM(str(model_input))

        #result = "Happy, 70%, Terminal"

        return Response({
            "feelings": {
                "anger": feelings[0],
                "disgust":feelings[1],
                "fear":feelings[2],
                "joy":feelings[3],
                "sadness":feelings[4],
            },
            "movies": {
                "movie_1": "NOT YET",
                "movie_2": "NOT YET",
                "movie_3": "NOT YET",
            },
            "options": {
                "movie_year": "movie_year",
                "rating": "rating",
            }


        })
