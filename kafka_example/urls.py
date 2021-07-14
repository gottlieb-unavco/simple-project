from django.urls import path
from kafka_example import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='kafka-example'),
]
