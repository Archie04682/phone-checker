from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

import config
from adapters import repository, source, cache
from adapters.endpoints import nt_phone_number_endpoint as ep


class AbstractUnitOfWork(ABC):
    numbers: repository.AbstractPhoneNumberRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri()
    )
)


def phone_source_factory() -> source.AbstractPhoneNumberSource:
    endpoint = ep.NTPhoneNumberEndpoint()
    return source.SingleEndpointPhoneNumberSource(endpoint)


def cache_factory(session: Session) -> cache.AbstractPhoneDataCache:
    return cache.PersistentPhoneDataCache(session, config.ACTUALITY_DELTA)


class SqlalchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.numbers = repository.PhoneNumberRepository(
            phone_source_factory(),
            cache_factory(self.session))
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
