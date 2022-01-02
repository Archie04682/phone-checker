from typing import Optional

from utils.number_formatter import NumberFormatter
from service_layer.unit_of_work import AbstractUnitOfWork


def get_number(digits: str, uow: AbstractUnitOfWork) -> Optional[dict]:
    with uow:
        formatted_digits = NumberFormatter.format(digits)
        if number := uow.numbers.get(formatted_digits):
            return number.as_dict()
        else:
            return None
