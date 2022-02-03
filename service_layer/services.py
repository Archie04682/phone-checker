from utils.number_formatter import NumberFormatter
from service_layer.unit_of_work import AbstractUnitOfWork
from domain.model import PhoneNumber
from adapters.cache import PhoneNumberNotFoundError, PhoneNumberOutdatedError
from adapters.gateway import PhoneDataLoadingError


class FailedToLoadPhoneNumberError(Exception):
    pass


def get_number(digits: str, uow: AbstractUnitOfWork) -> PhoneNumber:
    """
    Get PhoneNumber for the given digits.
    @param digits: str containing digits of the number to get.
    @param uow: AbstractUnitOfWork object to work with.
    @return: PhoneNumber object for the given digits.
    @raise service_layer.services.FailedToLoadPhoneNumberError if no valid phone number info in cache
    and failed to load the info from gateway.
    """
    with uow:
        formatted_digits = NumberFormatter.format(digits)
        try:
            number_to_return = uow.number_cache.get(formatted_digits)
        except (PhoneNumberNotFoundError, PhoneNumberOutdatedError):
            try:
                number_to_return = uow.number_gateway.get(formatted_digits)
                uow.number_cache.put(number_to_return)
                uow.commit()
            except PhoneDataLoadingError:
                raise FailedToLoadPhoneNumberError
        uow.expunge(number_to_return)
        return number_to_return
