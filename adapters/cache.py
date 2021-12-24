import abc
from typing import Optional
from domain.model.phone_number import PhoneNumber


class AbstractPhoneDataCache(abc.ABC):

    @abc.abstractmethod
    def put(self, digits: str, number: PhoneNumber):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, digits: str) -> Optional[PhoneNumber]:
        raise NotImplementedError
