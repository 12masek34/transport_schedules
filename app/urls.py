from django.urls import path
from .views import list_stations, station


urlpatterns = [
    path('<str:latitude>-<str:longitude>', list_stations, name='index'),
    path('<str:code>', station, name='index'),
]