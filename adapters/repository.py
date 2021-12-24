from abc import ABC, abstractmethod
from domain.model.phone_number import PhoneNumber


class AbstractPhoneDataRepository(ABC):

    @abstractmethod
    def get_phone_info(self, phone_number: str) -> PhoneNumber or None:
        raise NotImplementedError

    @abstractmethod
    def self_describe(self) -> str:
        raise NotImplementedError


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
