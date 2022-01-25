from utils.number_formatter import NumberFormatter
from service_layer.unit_of_work import AbstractUnitOfWork
from domain.model import PhoneNumber
from adapters.cache import CacheError


def get_number(digits: str, uow: AbstractUnitOfWork) -> PhoneNumber:
    """
    Get PhoneNumber for the given digits.
    @param digits: str containing digits of the number to get.
    @param uow: AbstractUnitOfWork object to work with.
    @return: PhoneNumber object for the given digits.
    @raise adapters.gateway.PhoneDataLoadingError if no valid phone number info in cache
    and failed to load the info from gateway.
    """
    with uow:
        formatted_digits = NumberFormatter.format(digits)
        try:
            return uow.number_cache.get(formatted_digits)
        except CacheError:
            new_version = uow.number_gateway.get(formatted_digits)
            uow.number_cache.put(new_version)
            return new_version
