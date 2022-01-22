from abc import ABC, abstractmethod
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Optional
from requests import get


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    body: Optional[str]


class AbstractHttpProvider(ABC):
    @abstractmethod
    def get(self, url: str, headers: [str]) -> HttpResponse:
        raise NotImplementedError


class HttpProvider(AbstractHttpProvider):
    @contextmanager
    def get(self, url: str, headers: [str]) -> HttpResponse:
        with get(url, headers=headers) as response:
            yield HttpResponse(response.status_code, response.text)
