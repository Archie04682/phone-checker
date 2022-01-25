from abc import ABC, abstractmethod
from datetime import timedelta, date
# from sqlalchemy.orm import Session

from domain.model import PhoneNumber


class PhoneNumberNotFoundError(Exception):
    pass


class PhoneNumberOutdatedError(Exception):
    pass


class AbstractPhoneNumberCache(ABC):
    @abstractmethod
    def put(self, number: PhoneNumber):
        raise NotImplementedError

    @abstractmethod
    def get(self, digits: str) -> PhoneNumber:
        raise NotImplementedError


class PgPhoneNumberPersistentCache(AbstractPhoneNumberCache):
    def __init__(self, session, actuality_delta: timedelta):
        self.session = session
        self.__actuality_delta = actuality_delta

    def put(self, number: PhoneNumber):
        """
        Store a PhoneNumber in the cache
        @param number: PhoneNumber object to store.
        """
        self.session.add(number)

    def get(self, digits: str) -> PhoneNumber:
        """
        Retrieve stored PhoneNumber from cache.
        @param digits: str containing digits of PhoneNumber to retrieve.
        @return: PhoneNumber object stored for the given digits.
        @raise PhoneNumberOutdatedError if the cache record for the given digits is outdated.
        @raise PhoneNumberNotFoundError if there's no record found for the given digits.
        """
        if found := self.session.query(PhoneNumber).filter_by(digits=digits).first():
            if self.__actuality_delta > date.today() - found.timestamp:
                return found
            raise PhoneNumberOutdatedError(f"Cache record for digits={digits} is outdated")
        raise PhoneNumberNotFoundError(f"Can't find cache record for digits={digits}")
