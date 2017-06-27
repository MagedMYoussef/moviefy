from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import generic
from moviefy_lstm.lstm_model import runLSTM
import requests
import json, re

# genres can be (Action-Adventure-Animation-Comedy-Crime-Documentary-Drama-Family-Fantasy
# History-Horror-Music-Mystery-Romance-Science Fiction-TV Movie-Thriller-War-Western)

def getGenreId(requiredGen):
    genres = {
        "Action": 28,
        "Adventure": 12,
        "Animation": 16,
        "Comedy": 35,
        "Crime": 80,
        "Documentary": 99,
        "Drama": 18,
        "Family": 10751,
        "Fantasy": 14,
        "History": 36,
        "Horror": 27,
        "Music": 10402,
        "Mystery": 9648,
        "Romance": 10749,
        "Science Fiction": 878,
        "TV Movie": 10770,
        "Thriller": 53,
        "War": 10752,
        "Western": 37, }

    return str(genres[requiredGen])


# genreId can be an array of genres ex: [53,12,27]
# rating is a number from 1 to 10

def getMovies(genreId, rating=8, startYear=2015, endYear=2017):
    Key = "4ea6a6403f897f25fc04b235768e15e4"
    url = "https://api.themoviedb.org/3/discover/movie?api_key=" + Key
    url = url + "&language=en-US&sort_by=popularity.desc&page=1"
    url = url + "&with_genres=" + str(genreId) + "&vote_average_gte=" + str(rating)
    url = url + "&release_date_gte=" + str(startYear) + "-1-1&release_date_lte=" + str(endYear) + "-1-1"

    payload = "{}"
    response = requests.request("GET", url, data=payload)
    return response.json()["results"][0:3]


def mapFeelingToMovieGenre(topFeeling):
    if (topFeeling == "Sadness"):
        genres = ["Comedy", "Family", "Fantasy"]
    elif (topFeeling == "Anger"):
        genres = ["Adventure", "Animation", "Drama"]
    elif (topFeeling == "Fear"):
        genres = ["Family", "Music"]
    elif (topFeeling == "Disgust"):
        genres = ["Fantasy", "Animation", "Music"]
    elif (topFeeling == "Joy"):
        genres = ["Comedy", "Romance", "Mystery"]

    str = ""
    for genre in genres:
        str = str + getGenreId(genre) + ","
    return str[0:-1]


def recommend(request):
    # Get the text the user typed to perform the algorithm on.
    # The template has a form that makes a POST request, we will go through this
    # request and get the value of the text entered
    if request.method == 'POST':
        post_request = request.POST
        '''
        Type of return from POST
        <QueryDict: {'csrfmiddlewaretoken': ['qeweqewr'], 'text-area1': ['I hate these new features On #ThisPhone after the update.']}>
        We well have key = 'text-area1', 'text-area2' or 'text-area3' based on where the user typed the text.
        '''
        text_area = dict(post_request.dict())
        '''
        Extracted text will be something like this
        ['I hate these new features On #ThisPhone after the update.']
        '''
        user_text = [value for key, value in text_area.items() if 'text-area' in key.lower()]

        '''
        if request.POST.get('text-area', False):
            user_text = str(request.POST['text-area'])
            #print ("My input text is " + user_text)  # watch your command line
        '''
        '''
        List of 5 Feelings returned from the LSTM Model
            "anger": feelings[0],
            "disgust":feelings[1],
            "fear":feelings[2],
            "joy":feelings[3],
            "sadness":feelings[4],
        '''
        feelings = runLSTM(str(user_text[0]))

        feelings = [float("{0:.2f}".format(f*100)) for f in feelings]
        '''
        Get Recommended Movies based on the top most feelings.
        '''
        top_feeling = feelings.index(max(feelings))
        feelings_list = ["Anger", "Disgust", "Fear", "Joy", "Sadness"]
        genres = mapFeelingToMovieGenre(feelings_list[top_feeling])
        # This will return a json object containing 3 movies.
        '''
        JSON Shape:
        [
          {
            "poster_path": "/gfJGlDaHuWimErCr5Ql0I8x9QSy.jpg",
            "title": "Wonder Woman",
            "overview": "An Amazon princess comes to the world of Man to become the greatest of the female superheroes.",
            "release_date": "2017-05-30",
            "popularity": 137.495481,
            "original_title": "Wonder Woman",
            "backdrop_path": "/hA5oCgvgCxj5MEWcLpjXXTwEANF.jpg",
            "vote_count": 1877,
            "video": false,
            "adult": false,
            "vote_average": 7,
            "genre_ids": [
              28,
              12,
              14,
              878
            ],
            "id": 297762,
            "original_language": "en"
          },
        ]
        '''

        movies_json = getMovies(genres)

        #print (json.dumps(movies_json, indent=2))
    # If the user came to this page using other methods than POST like GET request
    # we will redirect them to the original tryitout page to enter a new submission.
    # this can happen when the user access the page "http://127.0.0.1:8000/recommend/" directly
    # not as the usual way after submission.
    else:
        return redirect("try:index")

    # Construct a context to send the data to the template in order to be displayed.
    context = {
        'recommend': True,
        'feelings': feelings,
        'movies_json': movies_json,
        'user_text': user_text[0],
        'genres': genres, # genres dict,
    }

    '''
    TODO:
    [OK] This function will have to take the text user typed in the textarea
    [What we did] Template Passes the input text through variable called 'user_text' and this text is extracted from
    the textarea in the FORM
    [OK] We need to know which textarea box we are in ! .. the default now is the first box only.

    [NEXT] ** We will need to create a new App for the machine learning model and create an API for it.
    Then process the algorithm on this text to determine:
    1- Feelings map
    2- Top 3 recommended movies
    Then it send back the feelings map data and recommended movies to render the page again

    '''

    return render(request, 'recommend.html', context)

