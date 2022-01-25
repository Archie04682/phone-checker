from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from config import REPOSITORY_ACTUALITY_DELTA, get_postgres_uri
from adapters import gateway, cache
from adapters.loaders import nt_phone_number_loader as ep
from utils.http_provider import HttpProvider


class AbstractUnitOfWork(ABC):
    number_gateway: gateway.AbstractPhoneNumberGateway
    number_cache: cache.AbstractPhoneNumberCache

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
        get_postgres_uri(),
        isolation_level="REPEATABLE READ"
    )
)


def number_gateway_factory() -> gateway.AbstractPhoneNumberGateway:
    loader = ep.NTPhoneNumberLoader(HttpProvider())
    return gateway.SingleEndpointPhoneNumberGateway(loader)


def number_cache_factory(session: Session) -> cache.AbstractPhoneNumberCache:
    return cache.PgPhoneNumberPersistentCache(session, REPOSITORY_ACTUALITY_DELTA)


class SqlalchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.number_gateway = number_gateway_factory()
        self.number_cache = number_cache_factory(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
