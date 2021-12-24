from abc import ABC, abstractmethod


class AbstractPhoneNumberSource(ABC):

    @abstractmethod
    def get(self, digits: str):
        raise NotImplementedError
