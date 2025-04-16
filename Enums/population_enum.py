from enum import Enum


class PopulationEnum(str, Enum):
    SMALL = '۵ تا ۲۰ نفر'
    MEDIUM = '۲۰ تا ۵۰ نفر'
    LARGE = '۵۰ تا ۱۰۰ نفر'
    VERY_LARGE = '۱۰۰ نفر به بالا'
