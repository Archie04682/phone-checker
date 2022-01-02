from abc import ABC, abstractmethod
from typing import Optional
from datetime import timedelta, datetime
# from sqlalchemy.orm import Session

from domain.model import PhoneNumber


class AbstractPhoneDataCache(ABC):

    @abstractmethod
    def put(self, digits: str, number: PhoneNumber):
        raise NotImplementedError

    @abstractmethod
    def get(self, digits: str) -> Optional[PhoneNumber]:
        raise NotImplementedError


class PersistentPhoneDataCache(AbstractPhoneDataCache):

    def __init__(self, session, actuality_delta: timedelta):
        self.session = session
        self.__actuality_delta = actuality_delta

    def put(self, digits: str, number: PhoneNumber):
        self.session.add(number)

    def get(self, digits: str) -> Optional[PhoneNumber]:
        found = self.session.query(PhoneNumber).filter_by(digits=digits).one()
        return found if found and self.__actuality_delta < datetime.now() - found.timestamp else None
