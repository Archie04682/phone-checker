from typing import Optional
from random import choice

from adapters.data_source import AbstractPhoneNumberDataSource
from domain.model import PhoneNumber
from service_layer.services import get_number, AbstractUnitOfWork
from tests.random_generators import random_phone_number, random_phone_numbers


class FakePhoneDataSource(AbstractPhoneNumberDataSource):
    def __init__(self, data: [PhoneNumber]):
        self._data = data

    def get(self, digits: str) -> Optional[PhoneNumber]:
        return next((item for item in self._data if item.ref == digits), None)

    def set(self, phone_number: PhoneNumber):
        if found := next((item for item in self._data if item.ref == phone_number.ref), None):
            self._data.remove(found)
        self._data.append(phone_number)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, numbers_source: AbstractPhoneNumberDataSource):
        self.numbers = numbers_source
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def prepare():
    numbers = [num for num, _ in random_phone_numbers(3)]
    data_source = FakePhoneDataSource(numbers)
    uow = FakeUnitOfWork(data_source)
    return numbers, uow


def test_can_get_existing_number():
    existing_numbers, uow = prepare()
    num_to_find = choice(existing_numbers)
    found = get_number(num_to_find.ref, uow)

    assert found is not None
    assert found["digits"] == num_to_find.ref


def test_returns_none_if_number_doesnt_exist():
    _, uow = prepare()
    not_existing_num, _ = random_phone_number()
    result = get_number(not_existing_num.ref, uow)

    assert result is None


def test_commits_on_success():
    nums, uow = prepare()
    num_to_find = choice(nums)
    _ = get_number(num_to_find.ref, uow)

    assert uow.committed


def test_doesnt_commit_on_fail():
    _, uow = prepare()
    not_existing_num, _ = random_phone_number()
    _ = get_number(not_existing_num.ref, uow)

    assert not uow.committed
