import requests
import logging
from bs4 import BeautifulSoup

from adapters.phone_data_source import PhoneDataSource
from adapters.neberitrubku.nt_phone_data_parser import NTPhoneDataParser
from adapters.invalid_document_structure_error import InvalidDocumentStructureError

# TODO: Move settings to some file of something...
from models.number import TelephoneNumber

NTRUBKU_HOST = "https://www.neberitrubku.ru/nomer-telefona"


class NTPhoneDataSource(PhoneDataSource):

    def __init__(self):
        self._parser = NTPhoneDataParser()

    def self_describe(self) -> str:
        return "neberitrubku_2192571f-01ef-4198-a508-2a92f717f735"

    def get_phone_info(self, phone_number: str) -> TelephoneNumber or None:
        with requests.get(f"{NTRUBKU_HOST}/{phone_number}") as response:
            if response.status_code != 200:
                return None

            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                parsing_result = self._parser.parse(soup)
            except InvalidDocumentStructureError:
                logging.error(f"Failed to parse response "
                              f"for request to {NTRUBKU_HOST}/{phone_number}.")
                return None

            logging.info(f"Request to {NTRUBKU_HOST}/{phone_number} "
                         f"loaded and parsed successfully.")
            return parsing_result
