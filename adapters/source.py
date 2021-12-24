from abc import ABC, abstractmethod
from typing import Optional

from domain.model.phone_number import PhoneNumber


class AbstractPhoneNumberEndpoint(ABC):
    @abstractmethod
    def load_json(self, digits: str) -> {}:
        raise NotImplementedError


class AbstractPhoneNumberSource(ABC):
    @abstractmethod
    def get(self, digits: str) -> Optional[PhoneNumber]:
        raise NotImplementedError


class SingleEndpointPhoneNumberSource(AbstractPhoneNumberSource):

    def __init__(self, endpoint: AbstractPhoneNumberEndpoint):
        self.endpoint = endpoint

    def get(self, digits: str) -> Optional[PhoneNumber]:
        if phone_json := self.endpoint.load_json(digits):
            return PhoneNumber.from_dict(phone_json)
        return None


# TODO: There will be more complex multi-endpoint sources with sophisticated merging logic.
