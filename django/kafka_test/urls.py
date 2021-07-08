from django.urls import path
from kafka_test import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='kafka-test'),
]
