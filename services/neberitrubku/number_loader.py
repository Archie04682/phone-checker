import requests
import logging
from bs4 import BeautifulSoup

import parsers.invalid_document_structure_error
from parsers.neberitrubku.number_page_parser import NumberPageParser

# TODO: Move settings to some file of something...
NTRUBKU_HOST = "https://www.neberitrubku.ru/nomer-telefona"


class NumberLoader:
    def __init__(self):
        self._parser = NumberPageParser()

    def load(self, number: str, trace_id: str):
        with requests.get(f"{NTRUBKU_HOST}/{number}") as response:
            if response.status_code != 200:
                logging.error(f"trace_id: {trace_id} = request to {NTRUBKU_HOST}/{number} "
                              f"returned bad status_code ({response.status_code})")
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                parse_result = self._parser.parse(soup)
            except parsers.invalid_document_structure_error.InvalidDocumentStructureError:
                logging.error(f"trace_id: {trace_id} = failed to parse response "
                              f"for request to {NTRUBKU_HOST}/{number}.")
                return None
            else:
                logging.info(f"trace_id: {trace_id} = request to {NTRUBKU_HOST}/{number} "
                             f"loaded and parsed successfully.")
            return parse_result
