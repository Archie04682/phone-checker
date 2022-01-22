from typing import Optional

from tests.random_generators import random_phone_number, random_digits
from domain.model import PhoneNumber
from adapters.gateway import SingleEndpointPhoneNumberGateway, AbstractPhoneNumberLoader


class FakePhoneNumberLoader(AbstractPhoneNumberLoader):

    def __init__(self, return_success: bool = True):
        self._return_success = return_success

    def load_phone_number(self, digits: str) -> Optional[PhoneNumber]:
        if self._return_success:
            some_phone_number, _ = random_phone_number()
            some_phone_number.digits = digits
            return some_phone_number
        return None


def test_uses_loader_to_get_right_phone_number():
    gateway = SingleEndpointPhoneNumberGateway(FakePhoneNumberLoader())
    digits_to_load = random_digits()
    loaded_number = gateway.get(digits_to_load)

    assert loaded_number is not None
    assert loaded_number.digits == digits_to_load


def test_passes_none_from_loaded_on_fail():
    gateway = SingleEndpointPhoneNumberGateway(
        FakePhoneNumberLoader(return_success=False))
    result = gateway.get(random_digits())

    assert result is None
