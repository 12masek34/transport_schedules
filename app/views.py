# Standard Library
import os

from http import HTTPStatus

# Third Party
import httpx

from django.http import HttpResponse
from dotenv import load_dotenv

# Library
from app.models import Station
from app.enums import TransportTypeEnum


load_dotenv()
API_KEY = os.getenv('API_KEY')


def  list_stations(request, latitude: str, longitude: str) ->  HttpResponse:
    # lat: str = '45.039268'
    # long: str = '38.987221'
    response = httpx.get(f'https://api.rasp.yandex.net/v3.0/nearest_stations/?apikey={API_KEY}&format=json&lat={latitude}&lng={longitude}&distance=50&lang=ru_RU')
    response.raise_for_status()
    stations = []
    update_fields = [
        'distance',
        'latitude',
        'longitude',
        'majority',
        'popular_title',
        'short_title',
        'station_type',
        'station_type_name',
        'title',
        'transport_type',
        'type',
    ]
    if response.status_code == HTTPStatus.OK:
        for station in response.json()['stations']:
            stations.append(
                Station(
                    code=station['code'],
                    distance=station['distance'],
                    latitude=station['lat'],
                    longitude=station['lng'],
                    majority=station['majority'],
                    popular_title=station['popular_title'],
                    short_title=station['short_title'],
                    station_type=station['station_type'],
                    station_type_name=station['station_type_name'],
                    title=station['title'],
                    transport_type= station['transport_type'],
                    type=station['type'],
                )
            )

    Station.objects.bulk_create(
        stations,
        update_conflicts=True,
        update_fields=update_fields,
        unique_fields=['code'],
    )
    station_list = []
    for station in stations:
        station_list.append(f'<br> <a href="{station.code}">{station.code}</a> {station.title} --- {station.station_type_name}')
    return HttpResponse(''.join(station_list))


def station(request, code: str):
    response = httpx.get(f'https://api.rasp.yandex.net/v3.0/schedule/?apikey={API_KEY}&station={code}&direction=all')
    response.raise_for_status()
    import pdb; pdb.set_trace();
    return HttpResponse(response.text)