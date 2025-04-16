from enum import Enum


class SalaryEnum(str, Enum):
    INTERN = "۵ تا ۱۰ میلیون تومان"
    JUNIOR = "۱۰ تا ۲۰ میلیون تومان"
    MIDLEVEL = "۲۰ تا ۴۰ میلیون تومان"
    SENIOR = "۴۰ میلیون به بالا"
    NEGOTIATED = "توافقی"