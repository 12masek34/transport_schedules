# Third Party
from http.client import CannotSendHeader
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    IntegerField,
    Model,
    SmallIntegerField,
    TimeField,
)
from django.utils.functional import unpickle_lazyobject

# Library
from app.enums import TransportTypeEnum


class Station(Model):
    """Станции."""

    code = CharField(
        'Код станции в системе кодирования Яндекс Расписаний.',
        max_length=20,
        unique=True,
    )
    distance = DecimalField(
        'Расстояние от указанной в запросе точки до полученной в ответе станции.',
        max_digits=25,
        decimal_places=15,
    )
    latitude = DecimalField(
        'Широта согласно WGS84',
        max_digits=15,
        decimal_places=13,
    )
    longitude =DecimalField(
        'Долгота согласно WGS84',
        max_digits=16,
        decimal_places=13,
    )
    majority = IntegerField(
        'Целое число, определяющее относительную важность станции в транспортном сообщении региона,'
        'где 1 — высшая важность (например, главный вокзал города).',
        blank=True,
        null=True,
    )
    popular_title = CharField(
        'Общепринятое название станции.',
        max_length=256,
        blank=True,
        null=True,
    )
    short_title = CharField(
        'Короткое название станции.',
        max_length=128,
        blank=True,
        null=True,
    )
    station_type = CharField(
        'Тип станции',
        max_length=128,
        blank=True,
        null=True,
    )
    station_type_name = CharField(
        'Тип станции',
        max_length=256,
        blank=True,
        null=True,
    )
    title = CharField(
        'Название станции.',
        max_length=256,
        blank=True,
        null=True,
    )
    transport_type = CharField(
        'Основной тип транспорта для данной станции.',
        choices=TransportTypeEnum.get_choice(),
        max_length=128,
        blank=True,
        null=True,
    )
    type = CharField(
        'Вид найденного пункта.',
        max_length=128,
        blank=True,
        null=True,
    )
    shedule = ForeignKey(
        'Schedule',
        on_delete=CASCADE,
        null=True,
        blank=True,
    )


class Schedule(Model):
    """Рейсы"""
    code = CharField(
        'Код станции в системе кодирования Яндекс Расписаний.',
        max_length=20,
        unique=True,
    )
    arrival = TimeField(
        'Время прибытия',
    )
    days = CharField(
        'Дни курсирования нитки',
        max_length=256,
    )
    departure = TimeField(
        'Время отправления',
    )
    except_days = CharField(
        'Дни, в которые нитка не курсирует',
        max_length=256,
        null=True,
        blank=True,
    )
    is_fuzzy = BooleanField(
        'Признак неточности времени отправления и времени прибытия.',
        default=True,
    )
    platform = CharField(
        'Платформа или путь, с которого отправляется рейс',
        max_length=256,
    )
    stops = CharField(
        'Станции следования рейса, на которых совершается остановка.',
        max_length=1000,
    )
    terminal = CharField(
        'Терминал аэропорта',
        max_length=256,
        null=True,
        blank=True,
    )
    thread = ForeignKey(
        'Thread',
        on_delete=CASCADE,
        null=True,
        blank=True,
    )


class Thread(Model):
    """Информация о нитке."""

    carrier = ForeignKey(
        'Carrier',
        on_delete=CASCADE,
    )
    express_type = CharField(
        'Признак экспресса или аэроэкспресса',
        max_length=50,
        null=True,
        blank=True,
    )
    number = CharField(
        'Номер рейса.',
        max_length=20,
    )
    short_title= CharField(
        'Короткое название нитки. ',
        max_length=256,
        null=True,
        blank=True,
    )
    title= CharField(
        'Короткое название нитки.',
        max_length=512,
        null=True,
        blank=True,
    )
    transport_subtype = ForeignKey(
        'TransportSubtype',
        on_delete=CASCADE,
        null=True,
        blank=True,
    )
    transport_type = CharField(
        'Тип транспортного средства.',
        choices=TransportTypeEnum.get_choice(),
        max_length=128,
        null=True,
        blank=True,
    )
    uid = CharField(
        'Идентификатор нитки, принятый в Яндекс Расписаниях.',
        max_length=100,
        null=True,
        blank=True,
        unique=True,
    )
    vehicle = CharField(
        'Название транспортного средства.',
        max_length=128,
        null=True,
        blank=True,
    )


class TransportSubtype(Model):
    """Информация о подтипе транспортного средства."""

    color = CharField(
        'Основной цвет транспортного средства в шестнадцатеричном формате.',
        max_length=20,
        null=True,
        blank=True,
    )
    code = CharField(
        'Код подтипа транспорта',
        max_length=128,
        unique=True,
        null=True,
        blank=True,
    )
    title = CharField(
        'Описание подтипа транспорта на естественном языке.',
        max_length=256,
        null=True,
        blank=True,
    )


class Carrier(Model):
    """Информация о перевозчике."""

    code = IntegerField(
        'Код перевозчика в системе кодирования Яндекс Расписаний.',
        unique=True,
    )
    title = CharField(
        'Название перевозчика.',
        max_length=256,
    )
    codes = ForeignKey(
        'OtherCarrierCode',
        on_delete=CASCADE,
        null=True,
        blank=True,
    )


class OtherCarrierCode(Model):
    """Список кодов перевозчика в других системах кодирования, поддерживаемых Яндекс Расписаниями."""

    icao = CharField(
        'Код перевозчика в системе кодирования ICAO',
        max_length=256,
        unique=True,
        blank=True,
        null=True,
    )
    sirena = CharField(
        'Код перевозчика в системе кодирования Sirena',
        max_length=256,
        unique=True,
        blank=True,
        null=True,
    )
    iata = CharField(
        'Код перевозчика в системе кодирования IATA.',
        max_length=256,
        unique=True,
        blank=True,
        null=True,
    )
