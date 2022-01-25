from abc import ABC, abstractmethod
from typing import Optional

from domain.model import PhoneNumber


class PhoneDataLoadingError(Exception):
    def __init__(self,
                 document_text: str,
                 message: str = "Number Info Not Found."):
        self.document_text = document_text
        super().__init__(message)


class AbstractPhoneNumberLoader(ABC):
    @abstractmethod
    def load_phone_number(self, digits: str) -> Optional[PhoneNumber]:
        raise NotImplementedError


class AbstractPhoneNumberGateway(ABC):
    @abstractmethod
    def get(self, digits: str) -> Optional[PhoneNumber]:
        raise NotImplementedError


class SingleEndpointPhoneNumberGateway(AbstractPhoneNumberGateway):

    def __init__(self, loader: AbstractPhoneNumberLoader):
        self.loader = loader

    def get(self, digits: str) -> Optional[PhoneNumber]:
        return self.loader.load_phone_number(digits)


# TODO: There will be more complex multi-endpoint sources with sophisticated merging logic.
