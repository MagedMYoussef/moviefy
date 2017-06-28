from django.db import models

class LSTM(models.Model):
    model_input = models.CharField(max_length=5000)
    start_year = models.IntegerField(default=2010)
    end_year = models.IntegerField(default=2017)
    rating = models.FloatField(default=7)
