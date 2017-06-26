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
sys.setdefaultencoding('utf-8')

'''
# Setting the parameters
'''
### EMBEDDING_FILE = 'GoogleNews-vectors-negative300.bin'
TRAINING_FILE = 'Sentences_25k_Tones_Labeled(Train).csv'
TESTING_FILE = 'Sentences_25k_Tones_Labeled(Test).csv'
MAX_SEQUENCE_LENGTH = 100
MAX_NB_WORDS = 200000



def runLSTM(input_text):
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
    return prediction[0].tolist()