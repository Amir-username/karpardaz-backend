from enum import Enum


class StatusEnum(str, Enum):
    PENDING = "در صف بررسی"
    OPEND = "توسط کارفرما دیده شد"
    APPROVED = "تایید اولیه"
    INTERVIEW = "تایید برای مصاحبه"
    REJECTED = "رد شده"