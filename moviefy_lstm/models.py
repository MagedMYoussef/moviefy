from django.db import models

class LSTM(models.Model):
    model_input = models.CharField(max_length=5000)
    movie_year = models.IntegerField(default=2017)
    rating = models.FloatField(default=4)

    feelings = models.CharField(max_length=500)
    recommended_movies = models.CharField(max_length=1000)
