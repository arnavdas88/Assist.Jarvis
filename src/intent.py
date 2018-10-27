import json
import re
import string
import unicodedata
from io import open

import nltk
import numpy as np
import pandas as pd
from keras.layers import LSTM, Dense, Embedding, Input
from keras.models import Model, Sequential
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

import preprocess

nltk.download('stopwords')


def IntentModel(model):
    model = model.lower()
    if model == "onehot":
        return OneHotModel
    elif model == "embeddings":
        return EmbeddingsModel
    else:
        print("{} does not exist".format(model))
        return None


class BaseIntentModel:
    def __init__(self):
        self.x_train = None
        self.y_train = None
        self.model = None
        self.history = None

    def train(self, optimizer='rmsprop', loss='categorical_crossentropy',
              batch_size=5, epochs=100, validation=0.0, summary=False, name = ''):
        if summary:
            self.model.summary()

        self.model.compile(optimizer, loss, metrics=['mae', 'categorical_accuracy'])
        self.history = self.model.fit(
            self.x_train, self.y_train,
            batch_size=batch_size, epochs=epochs,
            validation_split=validation)
        if not name == '':
          self.model.save_weights(name + '.intent.model.h5')
        
    def load(self, name):
      self.model.load_weights(name + '.intent.model.h5')
      
    def save(self, name):
      self.model.save_weights(name + '.intent.model.h5')

    def decode(self, input_sequence, output_word_model):
        output_tokens = self.model.predict(input_sequence)
        token_index = np.argmax(output_tokens[0])
        intent = output_word_model.index2word[token_index]
        confidence = max(output_tokens[0])
        return intent, confidence


class OneHotModel(BaseIntentModel):
    def __init__(self, x_train, y_train,
                 input_len, output_len,
                 latent_dim=128, activation='tanh'):
        self.x_train = x_train
        self.y_train = y_train
        self.model = \
            self.build_model(input_len, output_len, latent_dim, activation)

    def build_model(self, input_len, output_len, latent_dim, activation):
        model = Sequential()
        model.add(
            LSTM(latent_dim, activation=activation,
                 input_shape=(None, input_len)))
        model.add(Dense(36, activation = 'relu'))
        model.add(Dense(output_len, activation='softmax'))
        return model


class EmbeddingsModel(BaseIntentModel):
    def __init__(self, x_train, y_train,
                 input_dim, output_dim,
                 latent_dim=128, activation='tanh'):
        self.x_train = x_train
        self.y_train = y_train
        self.model = \
            self.build_model(input_dim, output_dim, latent_dim, activation)

    def build_model(self, input_dim, output_dim, latent_dim, activation):
        model = Sequential()
        model.add(Embedding(input_dim, output_dim,))
        model.add(
            LSTM(latent_dim, activation=activation,
                 input_shape=(None, input_dim)))
        model.add(Dense(36, activation = 'relu'))
        model.add(Dense(output_dim, activation='softmax'))
        return model
