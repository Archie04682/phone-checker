import pytest
from sqlalchemy.orm import Session

from tests.conftest import insert_phone_number, get_phone_number
from domain.model import PhoneNumber
from tests.random_generators import random_phone_number, random_digits
from adapters.cache import PgPhoneNumberPersistentCache, PhoneNumberOutdatedError, PhoneNumberNotFoundError
from config import REPOSITORY_ACTUALITY_DELTA


def prepare(session_factory) -> (Session, PgPhoneNumberPersistentCache, PhoneNumber):
    session = session_factory()
    cache = PgPhoneNumberPersistentCache(session, REPOSITORY_ACTUALITY_DELTA)
    number, _ = random_phone_number()
    return session, cache, number


def test_saves_phone_number_to_persistent_cache(in_memory_session_factory):
    session, cache, actual_number = prepare(in_memory_session_factory)
    cache.put(actual_number)
    session.commit()

    loaded_number = get_phone_number(session, actual_number.ref)
    assert actual_number.ref == loaded_number.ref


def test_loads_phone_number_from_persistent_cache(in_memory_session_factory):
    session, cache, actual_number = prepare(in_memory_session_factory)
    insert_phone_number(session, actual_number)
    session.commit()

    loaded_number = cache.get(actual_number.digits)
    assert actual_number.ref == loaded_number.ref


def test_saves_and_retrieves_all_fields_of_phone_number(in_memory_session_factory):
    session, cache, actual_number = prepare(in_memory_session_factory)

    cache.put(actual_number)
    session.commit()
    loaded_number = cache.get(actual_number.digits)
    assert actual_number == loaded_number


def test_raises_if_number_is_outdated(in_memory_session_factory):
    session, cache, outdated_number = prepare(in_memory_session_factory)
    outdated_number.timestamp = outdated_number.timestamp - REPOSITORY_ACTUALITY_DELTA
    insert_phone_number(session, outdated_number)
    session.commit()

    with pytest.raises(PhoneNumberOutdatedError):
        _ = cache.get(outdated_number.digits)


def test_raises_if_number_not_found_in_cache(in_memory_session_factory):
    session, cache, _ = prepare(in_memory_session_factory)

    with pytest.raises(PhoneNumberNotFoundError):
        _ = cache.get(random_digits())
