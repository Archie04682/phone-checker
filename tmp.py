

# import requests
# from bs4 import BeautifulSoup
# from parsers.neberitrubku.number_page_parser import NumberPageParser
import logging

from services.number_description_service import NumberDescriptionService
from adapters.neberitrubku.nt_phone_data_adapter import NTPhoneDataAdapter

logging.basicConfig(filename="log.txt", filemode='w', format='%(name)s - %(levelname)s - %(message)s')

srv = NumberDescriptionService([NTPhoneDataAdapter()])
res = srv.describe("89090005054")

print(res.as_dict())


# with requests.get("https://www.neberitrubku.ru/nomer-telefona/89090000062") as response:
# with requests.get("https://www.neberitrubku.ru/nomer-telefona/89090001291") as response:
#     response.raise_for_status()
#     doc = response.text
#
#     # print("Downloaded document:")
#     # print(doc)
#
#     soup = BeautifulSoup(doc, 'html.parser')
#
#     num = NumberPageParser.parse(soup)
#     print(num.overall_rating)
#     print(num.is_actual)
#
#     print(num.info.as_dict())
#     print()
#
#     for r in num.reviews:
#         print(r.as_dict())
#
#
# from services.number_description_service import NumberDescriptionService
#
# s = NumberDescriptionService()
# s.describe("8 (909)0001291")
