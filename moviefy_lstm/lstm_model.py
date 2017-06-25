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

'''
# Text preparation
# The function "text_to_wordlist" is from
# https://www.kaggle.com/currie32/quora-question-pairs/the-importance-of-cleaning-text
'''
def text_to_wordlist(text, remove_stopwords=False, stem_words=False):
    # Clean the text, with the option to remove stopwords and to stem words.

    # Convert words to lower case and split them
    text = text.lower().split()

    # Optionally, remove stop words
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]

    text = " ".join(text)

    # Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)

    # Optionally, shorten words to their stems
    if stem_words:
        text = text.split()
        stemmer = SnowballStemmer('english')
        stemmed_words = [stemmer.stem(word) for word in text]
        text = " ".join(stemmed_words)

    # Return a list of words
    return(text)



def runLSTM(input_text):
    # Clearing the session before starting processing
    K.clear_session()

    # input data
    texts = []
    # target outputs
    labels = []
    # use this for handling file locations
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with codecs.open(os.path.join(__location__, TRAINING_FILE), encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        for values in reader:
            texts.append(text_to_wordlist(values[0]))
            labels.append([float(values[1]),float(values[2]),float(values[3]),float(values[4]),float(values[5])])


    test_texts = []
    test_labels = []
    with codecs.open(os.path.join(__location__, TESTING_FILE), encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        for values in reader:
            test_texts.append(text_to_wordlist(values[0]))
            test_labels.append([float(values[1]),float(values[2]),float(values[3]),float(values[4]),float(values[5])])




    # Loading the Model from disk
    # load json and create model
    json_file = open(os.path.join(__location__, 'model_25k_20k_RNN_GPU_BS100_EPOCH200_CODE1.json'), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(os.path.join(__location__, 'model_25k_20k_RNN_GPU_BS100_EPOCH200_CODE1.h5'))


    ## UPDATE: Now working after we fit the new word seq into the old oneself.
    ## THIS IS NOT WORKING AS EXPECTED LIKE IN TESTING FILE
    ## the new example would have to encode words using the same integers and embed the integers into the same word mapping. ????

    # Tokenization
    tokenizer = Tokenizer(MAX_NB_WORDS)
    tokenizer.fit_on_texts(texts + test_texts)

    input_text = [input_text]

    sequences = tokenizer.texts_to_sequences(input_text)
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

    prediction = loaded_model.predict(data)
    #print(prediction)
    # This will return a list of predictions
    return prediction[0].tolist()
