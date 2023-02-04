
from collections.abc import Mapping, Sequence

from app.models import Station


def save_or_update_stations(stations: Sequence[Mapping]) -> Sequence[Station]:
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
                transport_type= station['transport_type'],
                type=station['type'],
            )
        )

    Station.objects.bulk_create(
        list_stations,
        update_conflicts=True,
        update_fields=update_fields,
        unique_fields=['code'],
    )

    return list_stations
