from abc import ABC, abstractmethod
from typing import Optional

from domain.model.phone_number import PhoneNumber
from adapters.cache import AbstractPhoneDataCache
from adapters.source import AbstractPhoneNumberSource


class InvalidDocumentStructureError(Exception):
    def __init__(self,
                 document_text: str,
                 message: str = "Invalid Document Structure."):
        self.document_text = document_text
        self.message = message
        super().__init__(self.message)


class PhoneDataNotFoundError(Exception):
    def __init__(self,
                 document_text: str,
                 message: str = "Number Info Not Found."):
        self.document_text = document_text
        self.message = message
        super().__init__(self.message)


class AbstractPhoneNumberRepository(ABC):

    @abstractmethod
    def get(self, ref: str) -> PhoneNumber or None:
        raise NotImplementedError

    @abstractmethod
    def set(self, phone_number: PhoneNumber):
        raise NotImplementedError


class PhoneNumberRepository(AbstractPhoneNumberRepository):

    def __init__(self, source: AbstractPhoneNumberSource, cache: Optional[AbstractPhoneDataCache]):
        self.source = source
        self.cache = cache

    def get(self, ref: str) -> PhoneNumber or None:
        pass

    def set(self, phone_number: PhoneNumber):
        pass
