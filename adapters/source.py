from abc import ABC, abstractmethod
from typing import Optional

from domain.model import PhoneNumber


class AbstractPhoneNumberEndpoint(ABC):
    @abstractmethod
    def load_phone_number(self, digits: str) -> Optional[PhoneNumber]:
        raise NotImplementedError


class AbstractPhoneNumberSource(ABC):
    @abstractmethod
    def get(self, digits: str) -> Optional[PhoneNumber]:
        raise NotImplementedError


class SingleEndpointPhoneNumberSource(AbstractPhoneNumberSource):

    def __init__(self, endpoint: AbstractPhoneNumberEndpoint):
        self.endpoint = endpoint

    def get(self, digits: str) -> Optional[PhoneNumber]:
        return self.endpoint.load_phone_number(digits)


# TODO: There will be more complex multi-endpoint sources with sophisticated merging logic.
