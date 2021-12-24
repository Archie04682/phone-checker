from requests import get
from logging import info
from typing import Optional
from datetime import date, datetime, timedelta

from bs4 import BeautifulSoup

from config import NTRUBKU_HOST
from adapters.source import AbstractPhoneNumberEndpoint
from adapters.repository import InvalidDocumentStructureError, PhoneDataNotFoundError


class __NTPhoneDataParser:
    @staticmethod
    def _weeks_str_to_datetime(weeks_string) -> date:
        weeks_str = weeks_string.split(" ", 1)[0].lower()
        if weeks_str == "один":
            weeks = 1
        else:
            weeks = int(weeks_str)
        return date.today() - timedelta(weeks=weeks)

    @staticmethod
    def _calc_overall_rating(ratings: {int: str}):
        if not ratings:
            return 0
        total = 0
        division_factor = 0
        for count, rating_string in ratings.items():
            division_factor += count
            if rating_string == "положительная":
                total += count * 5
            elif rating_string == "отрицательная":
                total += count * 1
            else:
                total += count * 3
                if rating_string != "нейтральная":
                    logging.info(f"Unknown rating string found: '{rating_string}'.")
        return total / division_factor if division_factor != 0 else total / 1

    @staticmethod
    def _parse_number_info(soup: BeautifulSoup) -> NumberInfo:

        if main_info_div := soup.find("div", class_="mainInfo"):
            pass
        else:
            raise InvalidDocumentStructureError(soup.text)

        if digits_found := main_info_div.select_one("div.mainInfoHeader div.number"):
            digits = digits_found.find(text=True, recursive=False).text.strip()
        else:
            raise InvalidDocumentStructureError(soup.text)

        meta_info = [' '.join(span.text.split()) for span in main_info_div.select("div.mainInfoHeader div.number span")]

        ratings_raw = [rating.text.split('x ') for rating in main_info_div.select("div.description div.ratings li")]
        ratings = {int(rating[0].strip()): rating[-1].strip() for rating in ratings_raw}

        categories_raw = [cat.text.split('x ') for cat in main_info_div.select("div.description div.categories li")]
        categories = {cat[0].strip(): cat[-1].strip() for cat in categories_raw}

        if description_found := main_info_div.select_one("div.description div.advanced div"):
            description = description_found.text.strip()
        else:
            logging.warning(f"Found no description for number: {digits}")
            description = ""

        return NumberInfo(
            digits,
            meta_info,
            ratings,
            categories,
            description
        )

    @staticmethod
    def _parse_number_reviews(soup: BeautifulSoup) -> [NumberReview]:

        try:
            reviews_raw = [review
                           for review
                           in soup.find_all("div", class_="review")
                           if "reviewNew" not in review.attrs["class"]]
        except KeyError:
            raise InvalidDocumentStructureError(soup.text)

        reviews = []
        last_seen_review_publish_date = None

        for review_raw in reviews_raw:
            try:
                if rating_found := review_raw.find("meta", {"itemprop": "ratingValue"}):
                    rating = int(rating_found.attrs["content"])
                else:
                    raise InvalidDocumentStructureError(soup.text)

                tags = [tag.text.strip() for tag in review_raw.find_all(class_="reviewTag")]

                publish_date_found = review_raw.find("time", {"itemprop": "datePublished"})
                if publish_date_found:
                    publish_date = datetime.fromisoformat(publish_date_found.attrs["datetime"]).date()
                    publish_date_is_precise = True
                else:
                    publish_date_is_precise = False
                    review_time_found = review_raw.find("span", class_="review_time")
                    if review_time_found:
                        publish_date = NTPhoneDataParser._weeks_str_to_datetime(review_time_found.text.strip())
                    else:
                        if last_seen_review_publish_date:
                            publish_date = last_seen_review_publish_date
                        else:
                            continue
                        # raise InvalidDocumentStructureError(soup.text)
                last_seen_review_publish_date = publish_date

                if author_found := review_raw.find("span", {"itemprop": "author"}):
                    author = author_found.text.strip()
                    if author == "НБТ Пользователь":
                        author = "Анонимно"
                else:
                    author = "Анонимно"

                if title_found := review_raw.find("span", {"itemprop": "name"}):
                    title = title_found.text.strip()
                else:
                    title = "Без заголовка"

                if body_found := review_raw.find("span", class_="review_comment"):
                    body = body_found.text.strip()
                else:
                    raise InvalidDocumentStructureError(soup.text)

            except InvalidDocumentStructureError:
                logging.warning(f"Skipped review due to invalid structure: {review_raw.text}")

            else:
                reviews.append(
                    NumberReview(
                        rating,
                        tags,
                        publish_date,
                        publish_date_is_precise,
                        author,
                        title,
                        body
                    )
                )

        return reviews

    @staticmethod
    def parse(soup: BeautifulSoup) -> TelephoneNumber:

        number_info = NTPhoneDataParser._parse_number_info(soup)
        reviews = NTPhoneDataParser._parse_number_reviews(soup)
        overall_rating = NTPhoneDataParser._calc_overall_rating(number_info.ratings)

        return TelephoneNumber(overall_rating, number_info, reviews)



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
