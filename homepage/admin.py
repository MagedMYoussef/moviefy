from django.contrib import admin
from .models import Movie

#admin.site.register(Movie)

# Custom admin class
class MovieAdmin(admin.ModelAdmin):
    # To display the content of the Movie in form of a list
    list_display = ('movie_name', 'poster_url', 'release_year', 'genre', 'rating', 'imdb_link', 'cast')
    list_filter = ('movie_name','release_year', 'genre', 'rating')


# Register the admin class with the associated model
admin.site.register(Movie, MovieAdmin)

