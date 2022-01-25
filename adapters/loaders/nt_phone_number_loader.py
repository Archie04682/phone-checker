from logging import info, warning
from datetime import date, datetime, timedelta

from bs4 import BeautifulSoup

from config import NTRUBKU_HOST
from adapters.gateway import AbstractPhoneNumberLoader
from adapters.gateway import PhoneDataLoadingError
from domain.model import PhoneNumber, NumberCategory
from domain.model import PhoneNumberReview, ReviewTag
from utils import number_formatter
from utils import http_provider as http


class InvalidDocumentStructureError(Exception):
    def __init__(self,
                 document_text: str,
                 message: str = "Invalid Document Structure."):
        self.document_text = document_text
        super().__init__(message)


class _NTPhoneDataParse:
    @staticmethod
    def _weeks_str_to_date(weeks_string) -> date:
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
                    info(f"Unknown rating string found: '{rating_string}'.")
        return total / division_factor if division_factor != 0 else total / 1

    @staticmethod
    def _parse_number_reviews(soup: BeautifulSoup) -> [PhoneNumberReview]:
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
                    info("Review has no rating")
                    rating = 0

                tags = [ReviewTag(tag.text.strip()) for tag in review_raw.find_all(class_="reviewTag")]

                publish_date_found = review_raw.find("time", {"itemprop": "datePublished"})
                if publish_date_found:
                    publish_date = datetime.fromisoformat(publish_date_found.attrs["datetime"]).date()
                    last_seen_review_publish_date = publish_date
                else:
                    review_time_found = review_raw.find("span", class_="review_time")
                    if review_time_found:
                        publish_date = _NTPhoneDataParse._weeks_str_to_date(review_time_found.text.strip())
                    else:
                        if last_seen_review_publish_date:
                            publish_date = last_seen_review_publish_date
                        else:
                            info("Review has no publish date - skipping")
                            continue

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
                    warning("Review has no body")
                    body = ""
                    # raise InvalidDocumentStructureError(soup.text)

            except InvalidDocumentStructureError:
                warning(f"Skipped review due to invalid structure: {review_raw.text}")

            else:
                reviews.append(
                    PhoneNumberReview(
                        rating,
                        tags,
                        publish_date,
                        author,
                        title,
                        body,
                        "neberitrubku"
                    )
                )

        return reviews

    @staticmethod
    def parse_phone_number(soup: BeautifulSoup) -> PhoneNumber:
        if main_info_div := soup.find("div", class_="mainInfo"):
            pass
        else:
            raise InvalidDocumentStructureError(soup.text)

        if digits_found := main_info_div.select_one("div.mainInfoHeader div.number"):
            digits = number_formatter.NumberFormatter.format(
                digits_found.find(text=True, recursive=False).text.strip())
        else:
            raise InvalidDocumentStructureError(soup.text)

        ratings_raw = [rating.text.split('x ') for rating in main_info_div.select("div.description div.ratings li")]
        ratings = {int(rating[0].strip()): rating[-1].strip() for rating in ratings_raw}

        categories_raw = [cat.text.split('x ') for cat in main_info_div.select("div.description div.categories li")]
        categories = [NumberCategory(cat_data[-1].strip()) for cat_data in categories_raw]

        if description_found := main_info_div.select_one("div.description div.advanced div"):
            description = description_found.text.strip()
        else:
            warning(f"Found no description for number: {digits}")
            description = None

        overall_rating = _NTPhoneDataParse._calc_overall_rating(ratings)
        reviews = _NTPhoneDataParse._parse_number_reviews(soup)

        return PhoneNumber(
            overall_rating,
            digits,
            categories,
            description,
            reviews
        )


class NTPhoneNumberLoader(AbstractPhoneNumberLoader):
    _heads = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36 '
    }

    def __init__(self, http_provider: http.AbstractHttpProvider, host: str = NTRUBKU_HOST):
        self.__http_prov = http_provider
        self.__host = host

    def load_phone_number(self, digits: str) -> PhoneNumber:
        """
        Loads PhoneNumber for the given digits.
        @param digits: Str with phone number digits to load info for.
        @return: PhoneNumber object containing info for the given digits.
        @raise: PhoneDataLoadingError if failed to load PhoneNumber for the given digits.
        """
        with self.__http_prov.get(f"{self.__host}/{digits}", self._heads) as response:
            if response.status_code != 200:
                raise PhoneDataLoadingError(response.body)
            try:
                soup = BeautifulSoup(response.body, 'html.parser')
                loaded_number = _NTPhoneDataParse.parse_phone_number(soup)
            except InvalidDocumentStructureError:
                raise PhoneDataLoadingError(f"Failed to parse response "
                      f"for request to {self.__host}/{digits}.")

            if loaded_number.digits != digits:
                raise PhoneDataLoadingError(f"Failed to load number info - "
                                            f"request/response digits mismatch.")

            info(f"Request to {self.__host}/{digits} "
                 f"loaded and parsed successfully.")
            return loaded_number
