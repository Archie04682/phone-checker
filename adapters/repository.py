from abc import ABC, abstractmethod
from typing import Optional

from domain.model import PhoneNumber
from adapters.cache import AbstractPhoneDataCache
from adapters.source import AbstractPhoneNumberSource


class InvalidDocumentStructureError(Exception):
    def __init__(self,
                 document_text: str,
                 message: str = "Invalid Document Structure."):
        self.document_text = document_text
        super().__init__(message)


class PhoneDataNotFoundError(Exception):
    def __init__(self,
                 document_text: str,
                 message: str = "Number Info Not Found."):
        self.document_text = document_text
        super().__init__(message)


class AbstractPhoneNumberRepository(ABC):

    @abstractmethod
    def get(self, digits: str) -> Optional[PhoneNumber]:
        raise NotImplementedError

    @abstractmethod
    def set(self, phone_number: PhoneNumber):
        raise NotImplementedError


class PhoneNumberRepository(AbstractPhoneNumberRepository):

    def __init__(self, source: AbstractPhoneNumberSource, cache: Optional[AbstractPhoneDataCache]):
        self.source = source
        self.cache = cache

    def get(self, digits: str) -> Optional[PhoneNumber]:
        if cached := self.cache.get(digits):
            return cached
        elif loaded := self.source.get(digits):
            self.set(loaded)
            return loaded
        return None

    def set(self, phone_number: PhoneNumber):
        if self.cache:
            self.cache.put(phone_number)
