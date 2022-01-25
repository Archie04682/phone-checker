import pytest
from random import choice

import adapters.gateway
from domain.model import PhoneNumber
from adapters.cache import AbstractPhoneNumberCache, PhoneNumberNotFoundError, PhoneNumberOutdatedError
from adapters.gateway import AbstractPhoneNumberGateway, PhoneDataLoadingError
from service_layer.services import get_number, AbstractUnitOfWork
from tests.random_generators import random_phone_number


class FakePhoneDataCache(AbstractPhoneNumberCache):
    def __init__(self, data: [PhoneNumber], outdated: bool = False):
        self._data = data
        self._outdated = outdated

    def put(self, number: PhoneNumber):
        if found := next((item for item in self._data if item.ref == number.ref), None):
            self._data.remove(found)
        self._data.append(number)

    def get(self, digits: str) -> PhoneNumber:
        if self._outdated:
            raise PhoneNumberOutdatedError()
        found = next((item for item in self._data if item.ref == digits), None)
        if not found:
            raise PhoneNumberNotFoundError()
        return found


class FakePhoneDataGateway(AbstractPhoneNumberGateway):
    def __init__(self, data: [PhoneNumber]):
        self._data = data

    def get(self, digits: str) -> PhoneNumber:
        if found := next((item for item in self._data if item.ref == digits), None):
            return found
        else:
            raise PhoneDataLoadingError("test document text")


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, cache: AbstractPhoneNumberCache, gateway: AbstractPhoneNumberGateway):
        self.number_cache = cache
        self.number_gateway = gateway
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def prepare(outdated_cache: bool = False):
    existing_numbers = [random_phone_number()[0] for _ in range(6)]
    cached_numbers = existing_numbers[:2]
    not_cached_numbers = existing_numbers[3:]
    gateway = FakePhoneDataGateway(existing_numbers)
    cache = FakePhoneDataCache(cached_numbers, outdated_cache)
    uow = FakeUnitOfWork(cache, gateway)
    return not_cached_numbers, cached_numbers, uow


def test_can_get_cached_number():
    _, cached_numbers, uow = prepare()
    num_to_find = choice(cached_numbers)
    found = get_number(num_to_find.ref, uow)

    assert found is not None
    assert found.ref == num_to_find.ref


def test_can_load_not_cached_number():
    not_cached_numbers, _, uow = prepare()
    num_to_find = choice(not_cached_numbers)
    found = get_number(num_to_find.ref, uow)

    assert found is not None
    assert found.ref == num_to_find.ref


def test_can_update_outdated_cached_number():
    _, cached_numbers, uow = prepare(outdated_cache=True)
    num_to_find = choice(cached_numbers)
    found = get_number(num_to_find.ref, uow)

    assert found is not None
    assert found.ref == num_to_find.ref


def test_raises_if_fails_to_get_number():
    _, _, uow = prepare()
    not_existing_num, _ = random_phone_number()

    with pytest.raises(adapters.gateway.PhoneDataLoadingError):
        _ = get_number(not_existing_num.ref, uow)


def test_commits_on_successful_cache_updating():
    _, cached_numbers, uow = prepare(outdated_cache=True)
    num_to_find = choice(cached_numbers)
    _ = get_number(num_to_find.ref, uow)

    assert uow.committed


def test_doesnt_commit_on_fail_while_updating_cache():
    _, _, uow = prepare()
    not_existing_num, _ = random_phone_number()

    with pytest.raises(PhoneDataLoadingError):
        _ = get_number(not_existing_num.ref, uow)

    assert not uow.committed


def test_doesnt_commit_if_gets_number_from_cache():
    _, cached_numbers, uow = prepare()
    num_to_find = choice(cached_numbers)
    _ = get_number(num_to_find.ref, uow)

    assert not uow.committed
