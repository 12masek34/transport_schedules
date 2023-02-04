
# Standard Library
import os

from collections.abc import Mapping, Sequence

# Third Party
import httpx

from dotenv import load_dotenv

# Library
from app.models import (
    Carrier,
    OtherCarrierCode,
    Schedule,
    Station,
    Thread,
    TransportSubtype,
)


load_dotenv()
API_KEY = os.getenv('API_KEY')


def get_stations(latitude: str, longitude: str) -> httpx.Response:
    """Получить станции по координатам"""
    return httpx.get(
        f'https://api.rasp.yandex.net/v3.0/nearest_stations/?apikey={API_KEY}&format=json&lat={latitude}&lng={longitude}&distance=50&lang=ru_RU'
    )


def get_schedule(code: str) -> httpx.Response:
    """Получить расписания станции."""
    return httpx.get(
        f'https://api.rasp.yandex.net/v3.0/schedule/?apikey={API_KEY}&station={code}&direction=all'
    )

def save_or_update_stations(stations: Sequence[Mapping]) -> None:
    """Обновляет или создает новые станции."""

    list_stations = []
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
    for station in stations:
        list_stations.append(
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
                transport_type=station['transport_type'],
                type=station['type'],
            )
        )

    Station.objects.bulk_create(
        list_stations,
        update_conflicts=True,
        update_fields=update_fields,
        unique_fields=['code'],
    )


def save_or_update_schedules(schedules: Sequence[Mapping], code: str) -> None:
    """Обновляет или создает расписание станции."""

    list_schedules = []
    update_fields = [
        'code',
        'arrival',
        'days',
        'departure',
        'except_days',
        'is_fuzzy',
        'platform',
        'stops',
        'terminal',
        'thread',
    ]
    for schedule in schedules:
        transport_subtype, created = TransportSubtype.objects.update_or_create(
            code=schedule['thread']['transport_subtype']['code'],
            defaults={
                'color': schedule['thread']['transport_subtype']['color'],
                'title': schedule['thread']['transport_subtype']['title'],
            },
        )
        transport_subtype.save()

        (
            other_carrier_code,
            created,
        ) = OtherCarrierCode.objects.update_or_create(
            iata=schedule['thread']['carrier']['codes']['iata'],
            icao=schedule['thread']['carrier']['codes']['icao'],
            sirena=schedule['thread']['carrier']['codes']['sirena'],
            defaults={
                'iata': schedule['thread']['carrier']['codes']['iata'],
                'icao': schedule['thread']['carrier']['codes']['icao'],
                'sirena': schedule['thread']['carrier']['codes']['sirena'],
            },
        )
        other_carrier_code.save()
        carrier, created = Carrier.objects.update_or_create(
            code=schedule['thread']['carrier']['code'],
            defaults={
                'title': schedule['thread']['carrier']['title'],
                'codes': other_carrier_code,
            },
        )
        carrier.save()
        thread, created = Thread.objects.update_or_create(
            uid=schedule['thread']['uid'],
            defaults={
                'carrier': carrier,
                'express_type': schedule['thread']['express_type'],
                'number': schedule['thread']['number'],
                'short_title': schedule['thread']['short_title'],
                'title': schedule['thread']['title'],
                'transport_type': schedule['thread']['transport_type'],
                'vehicle': schedule['thread']['vehicle'],
                'transport_subtype': transport_subtype,
            },
        )
        thread.save()

        schedule = Schedule(
            code=code,
            arrival=schedule['arrival'],
            days=schedule['days'],
            departure=schedule['departure'],
            except_days=schedule['except_days'],
            is_fuzzy=schedule['is_fuzzy'],
            platform=schedule['platform'],
            stops=schedule['stops'],
            terminal=schedule['terminal'],
            thread=thread,
        )
        list_schedules.append(schedule)

    Schedule.objects.bulk_create(
        list_schedules,
        update_conflicts=True,
        update_fields=update_fields,
        unique_fields=['code'],
    )


def create_line_station(code: str, title: str, station_type_name: str) -> str:
    """Создает удобочитаемую строку с информацией о станции."""
    return f'<br> <a href="{code}">{code}</a> {title} --- {station_type_name}'


def create_line_schedule(title: str, days: str, arrival: str, departure: str) -> str:
    """Создает удобочитаемую строку с информацией о расписании."""
    return f'<br>Маршрут: {title}<br>Расписание: {days}<br> Время прибытия: {arrival}<br> Время отправления: {departure}<br>'
