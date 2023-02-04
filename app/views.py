# Standard Library
import os

from http import HTTPStatus

# Third Party
import httpx

from django.http import HttpResponse
from dotenv import load_dotenv

# Library
from app.services import save_or_update_stations


load_dotenv()
API_KEY = os.getenv('API_KEY')


def  list_stations(request, latitude: str, longitude: str) ->  HttpResponse:
    """Список станций."""

    response = httpx.get(f'https://api.rasp.yandex.net/v3.0/nearest_stations/?apikey={API_KEY}&format=json&lat={latitude}&lng={longitude}&distance=50&lang=ru_RU')
    response.raise_for_status()
    if response.status_code == HTTPStatus.OK:
        stations = save_or_update_stations(response.json()['stations'])

    station_list = []
    for station in stations:
        station_list.append(f'<br> <a href="{station.code}">{station.code}</a> {station.title} --- {station.station_type_name}')
    return HttpResponse(''.join(station_list))


def station(request, code: str):

    response = httpx.get(f'https://api.rasp.yandex.net/v3.0/schedule/?apikey={API_KEY}&station={code}&direction=all')
    response.raise_for_status()
    import pdb; pdb.set_trace();
    return HttpResponse(response.text)