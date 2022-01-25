from sqlalchemy.orm import Session

from tests.conftest import insert_phone_number, get_phone_number
from domain.model import PhoneNumber
from tests.random_generators import random_phone_number, random_digits
from adapters.cache import PostgresPhoneNumberRepository
from config import REPOSITORY_ACTUALITY_DELTA


def prepare(session_factory) -> (Session, PostgresPhoneNumberRepository, PhoneNumber):
    session = session_factory()
    repository = PostgresPhoneNumberRepository(session, REPOSITORY_ACTUALITY_DELTA)
    number, _ = random_phone_number()
    return session, repository, number


def test_saves_phone_number_to_persistent_storage(in_memory_session_factory):
    session, repository, actual_number = prepare(in_memory_session_factory)
    repository.put(actual_number)
    session.commit()

    loaded_number = get_phone_number(session, actual_number.ref)
    assert actual_number.ref == loaded_number.ref


def test_loads_phone_number_from_persistent_storage(in_memory_session_factory):
    session, repository, actual_number = prepare(in_memory_session_factory)
    insert_phone_number(session, actual_number)
    session.commit()

    loaded_number = repository.get(actual_number.digits)
    assert actual_number.ref == loaded_number.ref


def test_saves_and_retrieves_all_fields_of_phone_number(in_memory_session_factory):
    session, repository, actual_number = prepare(in_memory_session_factory)

    repository.put(actual_number)
    loaded_number = repository.get(actual_number.digits)
    assert actual_number == loaded_number


def test_returns_none_if_number_is_outdated(in_memory_session_factory):
    session, repository, outdated_number = prepare(in_memory_session_factory)
    outdated_number.timestamp = outdated_number.timestamp - REPOSITORY_ACTUALITY_DELTA
    insert_phone_number(session, outdated_number)
    session.commit()

    result = repository.get(outdated_number.digits)
    assert result is None


def test_returns_none_if_number_doesnt_exist(in_memory_session_factory):
    session, repository, _ = prepare(in_memory_session_factory)

    result = repository.get(random_digits())
    assert result is None
