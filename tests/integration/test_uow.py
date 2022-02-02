import pytest

from tests.conftest import insert_phone_number, get_phone_number
from tests.random_generators import random_phone_number
from service_layer.unit_of_work import SqlalchemyUnitOfWork


def test_calls_factories_on_context_startup(in_memory_session_factory, fake_gateway_factory, fake_cache_factory):
    assert fake_gateway_factory.call_count == 0
    assert fake_cache_factory.call_count == 0

    uow = SqlalchemyUnitOfWork(in_memory_session_factory, fake_gateway_factory, fake_cache_factory)
    with uow:
        pass

    assert fake_gateway_factory.call_count == 1
    assert fake_cache_factory.call_count == 1


def test_can_save_phone_number(in_memory_session_factory):
    uow = SqlalchemyUnitOfWork(in_memory_session_factory)
    with uow:
        num_to_set, _ = random_phone_number()
        num_to_set_ref = num_to_set.ref
        uow.number_cache.put(num_to_set)
        uow.commit()

    session = in_memory_session_factory()
    retrieved_num = get_phone_number(session, num_to_set_ref)
    assert retrieved_num is not None


def test_can_retrieve_phone_number(in_memory_session_factory):
    session = in_memory_session_factory()
    num, _ = random_phone_number()
    insert_phone_number(session, num)

    uow = SqlalchemyUnitOfWork(in_memory_session_factory)
    with uow:
        retrieved_num = uow.number_cache.get(num.digits)
        assert retrieved_num is not None


def test_rolls_back_without_explicit_commit(in_memory_session_factory):
    uow = SqlalchemyUnitOfWork(in_memory_session_factory)
    with uow:
        num_to_set, _ = random_phone_number()
        uow.number_cache.put(num_to_set)

    session = in_memory_session_factory()
    retrieved_num = get_phone_number(session, num_to_set.ref)
    assert retrieved_num is None


def test_rolls_back_on_error(in_memory_session_factory):
    class TestException(Exception):
        pass

    uow = SqlalchemyUnitOfWork(in_memory_session_factory)
    with pytest.raises(TestException):
        with uow:
            num_to_set, _ = random_phone_number()
            uow.number_cache.put(num_to_set)
            raise TestException

    session = in_memory_session_factory()
    retrieved_num = get_phone_number(session, num_to_set.ref)
    assert retrieved_num is None


# TODO: Implement the stuff below after adding versioning to PhoneNumber aggregate:
def try_to_allocate():
    pass


@pytest.mark.skip(reason="The logic to test is yet to be implemented")
def test_concurrent_updates_to_same_version_are_not_allowed():
    pass
