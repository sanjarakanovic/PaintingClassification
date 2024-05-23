from django.urls import path
from .views import *

urlpatterns = [
    path('classifier', ClassifierView.as_view(), name = 'prediction')
]


