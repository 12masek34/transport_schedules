# Standard Library
import os

from http import HTTPStatus

# Third Party
import httpx

from django.http import HttpResponse

# Library
from app.services import save_or_update_stations
from app.services import get_stations
from app.services import create_line
from app.services import get_schedule
from app.services import save_or_update_schedules


def  list_stations(request, latitude: str, longitude: str) ->  HttpResponse:
    """Список станций."""
    response = get_stations(latitude, longitude)
    response.raise_for_status()
    if response.status_code == HTTPStatus.OK:
        stations = save_or_update_stations(response.json()['stations'])

    station_list_response = []
    for station in stations:
        station_list_response.append(create_line(station))
    return HttpResponse(''.join(station_list_response))


def station(request, code: str):
    """Расписание станции."""
    response = get_schedule(code)
    response.raise_for_status()
    if response.status_code == HTTPStatus.OK:
        stations = save_or_update_schedules(response.json()['schedule'], code)
    return HttpResponse(response.text)