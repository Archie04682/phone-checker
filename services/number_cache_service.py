import abc
from domain.number import TelephoneNumber


class NumberCacheService(abc.ABC):

    @abc.abstractmethod
    def put(self, digits: str, number: TelephoneNumber):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, digits: str) -> TelephoneNumber or None:
        raise NotImplementedError
