# Third Party
from django.contrib import admin

# Library
from app.models import Station


@admin.register(Station)
class NoteAdmin(admin.ModelAdmin):
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
