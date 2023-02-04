
class TransportTypeEnum:
    """Тип транспортного средства."""

    PLANE = 'plane'
    TRAIN = 'train'
    SUBURBAN = 'suburban'
    BUS = 'bus'
    WATER = 'water'
    HELICOPTER = 'helicopter'

    values = {
        PLANE: 'самолет',
        TRAIN: 'поезд',
        SUBURBAN: 'электричка',
        BUS: 'автобус',
        WATER: 'транспорт',
        HELICOPTER: 'вертолет.',
        }

    @classmethod
    def get_choice(cls):
        return list(cls.values.items())
