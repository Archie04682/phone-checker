import datetime

import pytest
import pickle
from os.path import dirname
from pathlib import Path
from contextlib import contextmanager

from tests.random_generators import random_digits
from utils.http_provider import AbstractHttpProvider, HttpResponse
from domain.model import PhoneNumber
from adapters.loaders.nt_phone_number_loader import NTRUBKU_HOST, NTPhoneNumberLoader
from adapters.gateway import PhoneDataLoadingError


actual_phone_number = pickle.loads(
    Path(f"{dirname(__file__)}/_files/nt_obj_sample.bin").read_bytes())  # type: PhoneNumber
actual_phone_number.timestamp = datetime.date.today()
actual_phone_number.reviews[2].publish_date = datetime.date.today() - datetime.timedelta(weeks=44)

fake_good_response = HttpResponse(
    200, Path(f"{dirname(__file__)}/_files/nt_html_sample.html").read_text("utf-8"))
fake_invalid_data_response = HttpResponse(
    200, Path(f"{dirname(__file__)}/_files/nt_html_sample_2.html").read_text("utf-8"))
fake_not_found_response = HttpResponse(404, "")
fake_internal_server_error_response = HttpResponse(500, "")


class FakeHttpProvider(AbstractHttpProvider):
    passed_url = None
    passed_headers = None

    def __init__(self, response: HttpResponse):
        self._response = response

    @contextmanager
    def get(self, url: str, headers: [str]) -> HttpResponse:
        self.passed_url = url
        self.passed_headers = headers
        yield self._response


# NTPhoneNumberLoader tests:


def test_passes_host_and_headers_to_http_provider():
    provider = FakeHttpProvider(fake_good_response)
    loader = NTPhoneNumberLoader(provider)
    digits = actual_phone_number.digits
    _ = loader.load_phone_number(digits)

    assert provider.passed_url == f"{NTRUBKU_HOST}/{digits}"
    assert provider.passed_headers is not None


def test_parses_http_result_and_returns_phone_number():
    provider = FakeHttpProvider(fake_good_response)
    loader = NTPhoneNumberLoader(provider)
    digits = actual_phone_number.digits
    loaded_phone_number = loader.load_phone_number(digits)

    assert actual_phone_number == loaded_phone_number


def test_raises_on_404():
    provider = FakeHttpProvider(fake_not_found_response)
    loader = NTPhoneNumberLoader(provider)

    with pytest.raises(PhoneDataLoadingError):
        _ = loader.load_phone_number(random_digits())


def test_raises_on_not_200():
    provider = FakeHttpProvider(fake_internal_server_error_response)
    loader = NTPhoneNumberLoader(provider)

    with pytest.raises(PhoneDataLoadingError):
        _ = loader.load_phone_number(random_digits())


def test_raises_on_digits_mismatch():
    provider = FakeHttpProvider(fake_invalid_data_response)
    loader = NTPhoneNumberLoader(provider)
    digits = actual_phone_number.digits

    with pytest.raises(PhoneDataLoadingError):
        _ = loader.load_phone_number(digits)
