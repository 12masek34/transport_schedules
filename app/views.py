# Third Party
from django.http import HttpResponse

# Library
from app.services import (
    create_line_schedule,
    create_line_station,
    get_schedule,
    get_stations,
    save_or_update_schedules,
    save_or_update_stations,
)

def list_stations(request, latitude: str, longitude: str) -> HttpResponse:
    """Список станций."""
    response = get_stations(latitude, longitude)
    response.raise_for_status()
    save_or_update_stations(response.json()['stations'])

    station_list_response = []
    for station in response.json()['stations']:
        code = station['code']
        title = station['title']
        station_type_name = station['station_type_name']
        station_list_response.append(
            create_line_station(code, title, station_type_name)
        )
    return HttpResponse(''.join(station_list_response))


def station(request, code: str):
    """Расписание станции."""
    response = get_schedule(code)
    response.raise_for_status()
    save_or_update_schedules(response.json()['schedule'], code)

    schedule_list_response = []
    for schedule in response.json()['schedule']:
        title = schedule['thread']['title']
        days = schedule['days']
        arrival = schedule['arrival']
        departure = schedule['departure']
        schedule_list_response.append(
            create_line_schedule(title, days, arrival, departure)
        )
    if not schedule_list_response:
        schedule_list_response = 'Ничего нет.'
    return HttpResponse(''.join(schedule_list_response))
