from django.apps import AppConfig
import os
from django.conf import settings
from keras.models import load_model
import keras
import tensorflow

class Model1Config(AppConfig):
    name = 'model1API'
    MODEL_FILE = os.path.join(settings.MODELS, 'model1.tf')
  #  model = keras.models.load_model(MODEL_FILE)
    model = tensorflow.saved_model.load(MODEL_FILE)

class Model2Config(AppConfig):
    name = 'model2API'
    MODEL_FILE = os.path.join(settings.MODELS, 'model2.tf')
    #model = keras.models.load_model(MODEL_FILE)
    model = tensorflow.saved_model.load(MODEL_FILE)
    

