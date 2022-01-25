import pytest

from config import NTRUBKU_HOST
from tests.random_generators import random_digits
from utils.http_provider import AbstractHttpProvider, HttpResponse
from domain.model import PhoneNumber
from adapters.loaders.nt_phone_number_loader import NTPhoneNumberLoader
from adapters.gateway import PhoneDataLoadingError


# TODO: Fill in response text and PhoneNumber constructor below:
# actual_phone_number = PhoneNumber()
fake_good_response = HttpResponse(200, "")
fake_not_found_response = HttpResponse(404, "")
fake_internal_server_error_response = HttpResponse(500, "")
fake_invalid_data_response = HttpResponse(200, "__digits should be different from those in actual_phone_number__")


class FakeHttpProvider(AbstractHttpProvider):
    passed_url = None
    passed_headers = None

    def __init__(self, response: HttpResponse):
        self._response = response

    def get(self, url: str, headers: [str]) -> HttpResponse:
        self.passed_url = url
        self.passed_headers = headers
        return self._response


# NTPhoneNumberLoader tests:


@pytest.mark.skip(reason="Not Implemented")
def test_passes_host_and_headers_to_http_provider():
    provider = FakeHttpProvider(fake_good_response)
    loader = NTPhoneNumberLoader(provider)
    digits = random_digits()
    loader.load_phone_number(digits)

    assert provider.passed_url == f"{NTRUBKU_HOST}/{digits}"
    assert provider.passed_headers is not None


@pytest.mark.skip(reason="Not Implemented")
def test_parses_http_result_and_returns_phone_number():
    provider = FakeHttpProvider(fake_good_response)
    loader = NTPhoneNumberLoader(provider)
    digits = actual_phone_number.digits
    loaded_phone_number = loader.load_phone_number(digits)

    assert actual_phone_number == loaded_phone_number


@pytest.mark.skip(reason="Not Implemented")
def test_raises_on_404():
    with pytest.raises(PhoneDataLoadingError):
        provider = FakeHttpProvider(fake_not_found_response)
        loader = NTPhoneNumberLoader(provider)
        _ = loader.load_phone_number(random_digits())


@pytest.mark.skip(reason="Not Implemented")
def test_raises_on_not_200():
    with pytest.raises(PhoneDataLoadingError):
        provider = FakeHttpProvider(fake_internal_server_error_response)
        loader = NTPhoneNumberLoader(provider)
        _ = loader.load_phone_number(random_digits())


@pytest.mark.skip(reason="Not Implemented")
def test_raises_on_digits_mismatch():
    with pytest.raises(PhoneDataLoadingError):
        provider = FakeHttpProvider(fake_invalid_data_response)
        loader = NTPhoneNumberLoader(provider)
        digits = actual_phone_number.digits
        _ = loader.load_phone_number(digits)
