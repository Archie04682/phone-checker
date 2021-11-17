from abc import ABC, abstractmethod
from models.number import TelephoneNumber


class PhoneDataSource(ABC):

    @abstractmethod
    def get_phone_info(self, phone_number: str) -> TelephoneNumber or None:
        raise NotImplementedError

    @abstractmethod
    def self_describe(self) -> str:
        raise NotImplementedError
