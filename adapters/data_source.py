# from abc import ABC, abstractmethod
# from typing import Optional
#
# from domain.model import PhoneNumber
# from adapters.cache import AbstractPhoneNumberCache
# from adapters.gateway import AbstractPhoneNumberGateway
#
#
# class AbstractPhoneNumberDataSource(ABC):
#
#     @abstractmethod
#     def get(self, digits: str) -> Optional[PhoneNumber]:
#         raise NotImplementedError
#
#     @abstractmethod
#     def set(self, phone_number: PhoneNumber):
#         raise NotImplementedError
#
#
# class PhoneNumberDataSource(AbstractPhoneNumberDataSource):
#     def __init__(self,
#                  gateway: AbstractPhoneNumberGateway,
#                  cache: Optional[AbstractPhoneNumberCache]):
#         self.gateway = gateway
#         self.cache = cache
#
#     def get(self, digits: str) -> Optional[PhoneNumber]:
#         if cached := self.cache.get(digits):
#             return cached
#         elif loaded := self.gateway.get(digits):
#             self.set(loaded)
#             return loaded
#         return None
#
#     def set(self, phone_number: PhoneNumber):
#         if self.cache:
#             self.cache.put(phone_number)
