from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from config import REPOSITORY_ACTUALITY_DELTA, get_postgres_uri
from adapters import data_source, gateway, cache
from adapters.loaders import nt_phone_number_loader as ep
from utils.http_provider import HttpProvider


class AbstractUnitOfWork(ABC):
    numbers: data_source.AbstractPhoneNumberDataSource

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


def phone_gateway_factory() -> gateway.AbstractPhoneNumberGateway:
    loader = ep.NTPhoneNumberLoader(HttpProvider())
    return gateway.SingleEndpointPhoneNumberGateway(loader)


def phone_repository_factory(session: Session) -> repository.AbstractPhoneNumberRepository:
    return repository.PostgresPhoneNumberRepository(session, REPOSITORY_ACTUALITY_DELTA)


class SqlalchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.numbers = data_source.PhoneNumberDataSource(
            phone_gateway_factory(),
            phone_repository_factory(self.session))
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
