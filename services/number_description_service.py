import logging
from logging import Logger
from typing import Optional

from domain.number import TelephoneNumber
from adapters.repository import AbstractPhoneDataRepository
from services.number_cache_service import NumberCacheService
from services.number_normalize_service import NumberNormalizeService


class NumberDescriptionService:
    def __init__(self,
                 cache_service: NumberCacheService,
                 phone_data_sources: [AbstractPhoneDataRepository],
                 logger: Logger = None):
        self._phone_data_sources = phone_data_sources
        self._cache = cache_service
        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger()

    def describe(self, number: str) -> Optional[TelephoneNumber]:
        normalized_number = NumberNormalizeService.normalize(number)
        if cached_description := self._cache.get(normalized_number):
            description = cached_description
            self._logger.info(f"Retrieved cached version for {number}")
        else:
            description = self._describe(number)
            self._cache.put(normalized_number, description)
            self._logger.info(f"Requested new version for {number}")
        return description

    def _describe(self, number: str):
        # TODO: Organize merging of different data_sources' results
        # For now we have only 1 source  so no need to merge:
        if self._phone_data_sources is None:
            return None
        return self._phone_data_sources[0].get_phone_info(number)

