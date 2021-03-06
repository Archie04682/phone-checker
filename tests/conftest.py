import pytest
from datetime import date
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from adapters.orm import mapper_registry, start_mappers
from domain.model import PhoneNumber


def insert_phone_number(session, number: PhoneNumber):
    # noinspection SqlNoDataSourceInspection,SqlResolve
    session.execute(
        "INSERT INTO phone_numbers (rating, digits, description, timestamp) "
        "VALUES (:rating, :digits, :description, :timestamp)",
        {"rating": number.rating,
         "digits": number.digits,
         "description": number.description,
         "timestamp": number.timestamp})


def get_phone_number(session, ref: str) -> Optional[PhoneNumber]:
    # noinspection SqlNoDataSourceInspection,SqlResolve
    rows = session.execute("SELECT * FROM phone_numbers WHERE digits=:ref", {"ref": ref})
    if row := rows.first():
        return PhoneNumber(rating=row.rating,
                           digits=row.digits,
                           categories=[],
                           description=row.description,
                           reviews=[],
                           timestamp=date.fromisoformat(row.timestamp))
    return None


def get_table_rows_count(session) -> int:
    # noinspection SqlNoDataSourceInspection,SqlResolve
    [[row_count]] = session.execute("SELECT count(*) FROM phone_numbers")
    return row_count


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def in_memory_session_factory(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def in_memory_session(session_factory):
    return session_factory()


@pytest.fixture
def fake_gateway_factory():
    class FakeGatewayFactory:
        call_count = 0

        def __call__(self):
            self.call_count += 1

    yield FakeGatewayFactory()


@pytest.fixture
def fake_cache_factory():
    class FakeCacheFactory:
        call_count = 0

        def __call__(self, _):
            self.call_count += 1

    yield FakeCacheFactory()
