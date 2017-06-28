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

import sys

reload(sys)

'''
# Setting the parameters
'''
MAX_SEQUENCE_LENGTH = 100
MAX_NB_WORDS = 200000

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

def getMovies(genreId, rating=8, startYear=1994, endYear=2017):
    Key = "4ea6a6403f897f25fc04b235768e15e4"
    url = "https://api.themoviedb.org/3/discover/movie?api_key=" + Key
    url = url + "&language=en-US&sort_by=popularity.desc&page=1"
    url = url + "&with_genres=" + str(12) + "&vote_average_gte=" + str(rating)
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


def runLSTM(input_text, rating, startYear, endYear):
    # Clearing the session before starting processing
    K.clear_session()

    # use this for handling file locations
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

    movies_json = getMovies(genres, rating, startYear, endYear)

    # list of returned data
    data = [feelings, movies_json]
    return data
