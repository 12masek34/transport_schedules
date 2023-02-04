# Third Party
from django.contrib import admin

# Library
from app.models import Station, Schedule, Thread, TransportSubtype, Carrier, OtherCarrierCode


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = [
        'code',
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


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'arrival',
        'departure',
    ]


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = [
        'number',
        'title',
    ]

@admin.register(TransportSubtype)
class TransportSubtypeAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'color',
    ]


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'title',
    ]

@admin.register(OtherCarrierCode)
class OtherCarrierCodeAdmin(admin.ModelAdmin):
    list_display = [
        'icao',
        'sirena',
    ]
