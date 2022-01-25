from abc import ABC, abstractmethod
from typing import Optional

from domain.model import PhoneNumber
from adapters.cache import AbstractPhoneNumberRepository
from adapters.gateway import AbstractPhoneNumberGateway








class AbstractPhoneNumberDataSource(ABC):

    @abstractmethod
    def get(self, digits: str) -> Optional[PhoneNumber]:
        raise NotImplementedError

    @abstractmethod
    def set(self, phone_number: PhoneNumber):
        raise NotImplementedError


class PhoneNumberDataSource(AbstractPhoneNumberDataSource):
    def __init__(self,
                 gateway: AbstractPhoneNumberGateway,
                 repository: Optional[AbstractPhoneNumberRepository]):
        self.gateway = gateway
        self.repository = repository

    def get(self, digits: str) -> Optional[PhoneNumber]:
        if cached := self.repository.get(digits):
            return cached
        elif loaded := self.gateway.get(digits):
            self.set(loaded)
            return loaded
        return None

    def set(self, phone_number: PhoneNumber):
        if self.repository:
            self.repository.put(phone_number)
