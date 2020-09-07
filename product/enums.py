from enum import Enum


class MeasureTypes(Enum):
    kg = 'kilogramm'
    ta = 'dona'
    m = 'metr'
    l = 'litr'

    @classmethod
    def choices(cls):
        return tuple((choice.name, choice.value) for choice in cls)
