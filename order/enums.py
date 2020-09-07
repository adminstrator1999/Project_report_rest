from enum import Enum


class OrderTypes(Enum):
    selling = "selling"
    buying = "buying"

    @classmethod
    def choices(cls):
        return tuple((choice.name, choice.value) for choice in cls)




