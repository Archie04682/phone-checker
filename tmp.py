

import requests
from bs4 import BeautifulSoup
from parsers.neberitrubku.number_page_parser import NumberPageParser

# with requests.get("https://www.neberitrubku.ru/nomer-telefona/89090000062") as response:
with requests.get("https://www.neberitrubku.ru/nomer-telefona/89090001291") as response:
    response.raise_for_status()
    doc = response.text

    # print("Downloaded document:")
    # print(doc)

    soup = BeautifulSoup(doc, 'html.parser')

    num = NumberPageParser.parse(soup)
    print(num.info.meta_info)
    print(num.info.digits)
    print(num.info.ratings)
    print(num.info.categories)
    print(num.info.description)

    for r in num.reviews:
        print("\n")
        print(r.rating)
        print(r.tags)
        print(r.publish_date)
        if r.publish_date_is_precise:
            print("Precise date")
        else:
            print("Approx date")
        print(r.author)
        print(r.title)
        print(r.body)



# TODO: Нормализовать номер - это лучше делать когда он приходит в запросе от клиента
# TODO: Вычислить общий рейтинг номера и его актуальность
