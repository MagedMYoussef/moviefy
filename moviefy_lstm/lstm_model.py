# -*- coding: utf-8 -*-
import os
import re
import csv
import codecs

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from keras.preprocessing.text import Tokenizer
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
from keras import backend as K
from moviefy_lstm.apps import tokenizer
import tmdbsimple as tmdb
import json

tmdb.API_KEY = '4ea6a6403f897f25fc04b235768e15e4'

import sys

reload(sys)

'''
# Setting the parameters
'''
MAX_SEQUENCE_LENGTH = 100
MAX_NB_WORDS = 200000

import requests
import json, re
import random

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

def getMovies(genreIds, rating=8, startYear=2014, endYear=2017):
    """
    Limitation: we can only retrieve one page
        and each page contains only 20 movies
    What we will do:
        We will randomize page selection each time using a random number from 1 to 5
        and also randomize the number that is used within the page from 1 to 20 ... response.json()["results"][0:3]
    """
    # Directly using requests:
    Key = "4ea6a6403f897f25fc04b235768e15e4"
    url = "https://api.themoviedb.org/3/discover/movie?api_key="+Key
    url = url + "&language=en-US&sort_by=popularity.desc&page=1&include_adult=false"
    url = url + "&with_genres="+str(genreIds)+"&vote_average.gte="+str(rating)
    url = url + "&release_date.gte="+ str(startYear) + "-1-1&release_date.lte="+ str(endYear)+"-12-30"
    url = url + "&page=" + str(random.randint(0,5)) # Random Number from 0 to 5

    payload = "{}"
    response = requests.request("GET", url, data=payload)
    # Each time we will return a randomized sublist from the page we are in, selecting a random list of 3 elements
    return random.sample(response.json()["results"], 3)

    '''
    Or By Simply using a library
    discover = tmdb.Discover()
    response = discover.movie(page=1, language="en-US", sort_by='popularity.desc', with_genres=12, vote_average_gte=rating, vote_count_gte=50,
                              release_date_gte=str(startYear)+"-1-1", release_date_lte=str(endYear)+"-12-30")

    return response["results"][0:3]
    '''

def mapFeelingToMovieGenre(topFeeling):
    if (topFeeling == "Sadness"):
        genres = ["Comedy", "Family", "Fantasy"]
    elif (topFeeling == "Anger"):
        genres = ["Adventure", "Drama"]
    elif (topFeeling == "Fear"):
        genres = ["Family","Comedy","Adventure"]
    elif (topFeeling == "Disgust"):
        genres = ["Fantasy", "Music"]
    elif (topFeeling == "Joy"):
        genres = ["Comedy", "Romance", "Mystery", "Adventure"]

    str = ""
    for genre in genres:
        # "%2C" for all genres inclusive like Comedy && Family && Fantasy
        # "%7C" for anyone of them like Comedy || Family || Fantasy
        str = str + getGenreId(genre) + "%7C"
    return str[0:-1]


def runLSTM(input_text, rating, startYear, endYear):
    # Clearing the session before starting processing
    K.clear_session()

    # use this for handling file locations -Get the current directory
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Loading the Model from disk
    # load json and create model
    json_file = open(os.path.join(__location__, 'model_25k_20k_RNN_GPU_BS100_EPOCH200_CODE1.json'), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(os.path.join(__location__, 'model_25k_20k_RNN_GPU_BS100_EPOCH200_CODE1.h5'))

    input_text = [input_text]

    sequences = tokenizer.texts_to_sequences(input_text)
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

    # List of 5 feelings
    prediction = loaded_model.predict(data)
    # print(prediction)
    # This will return a list of predictions

    # Feelings map
    feelings = prediction[0].tolist()
    feelings = [float("{0:.2f}".format(f * 100)) for f in feelings]
    '''
    Get Recommended Movies based on the top most feelings.
    '''
    top_feeling = feelings.index(max(feelings))
    feelings_list = ["Anger", "Disgust", "Fear", "Joy", "Sadness"]
    genres = mapFeelingToMovieGenre(feelings_list[top_feeling])

    # This will return a json object containing 3 movies.
    '''
    JSON Shape:
    [ "results":
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

    movies_json = getMovies(genres, rating, startYear, endYear)

    # list of returned data
    data = [feelings, movies_json]

    return data
