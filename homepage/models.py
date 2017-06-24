from django.db import models

class Movie(models.Model):
    """
    This Model will represent Moviefy movies database.
    It includes (movie_name, poster_url, release_year, genre, rating, imdb_link, cast)
    """
    movie_name = models.CharField(max_length=100)
    poster_url = models.CharField(max_length=1000)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    rating = models.FloatField(max_length=5)
    imdb_link = models.CharField(max_length=1000)
    cast = models.CharField(max_length=1000)

    def __str__(self):
        """
        String to represent the Model object
        """
        return (self.movie_name + " (" +str(self.release_year)+")")

