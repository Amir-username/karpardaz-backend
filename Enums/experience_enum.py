from enum import Enum


class ExperienceEnum(str, Enum):
    NO_EXPERIENSE = "بدون سابقه کار"
    SHORT_EXPERIENCE = "۱ تا ۲ سال سابفه کار"
    MEDIUM_EXPERIENEC = "۲ تا ۴ سال سابقه کار"
    LONG_EXPERIENCE = "۴ سال به بالا"
