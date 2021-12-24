import requests
import logging
from bs4 import BeautifulSoup
from typing import Optional

from adapters.repository import AbstractPhoneDataRepository
from adapters.neberitrubku.nt_phone_data_parser import NTPhoneDataParser
from adapters.exceptions import InvalidDocumentStructureError, PhoneDataNotFoundError

# TODO: Move settings to some file of something...
from domain.number import TelephoneNumber

NTRUBKU_HOST = "https://www.neberitrubku.ru/nomer-telefona"


class NTPhoneDataSource(AbstractPhoneDataRepository):
    def __init__(self):
        self._parser = NTPhoneDataParser()

    def self_describe(self) -> str:
        return "neberitrubku_2192571f-01ef-4198-a508-2a92f717f735"

    def get_phone_info(self, phone_number: str) -> Optional[TelephoneNumber]:
        heads = {
            # ":authority": 'www.neberitrubku.ru',
            # ':method': 'GET',
            # ':path': f'/nomer-telefona/{phone_number}',
            # ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'sec-ch-ua': 'Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }

        with requests.get(f"{NTRUBKU_HOST}/{phone_number}", headers=heads) as response:

            if response.status_code == 404:
                raise PhoneDataNotFoundError(response.text)

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
