from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import logging

from adapters.invalid_document_structure_error import InvalidDocumentStructureError
from models.number_info import NumberInfo
from models.number_review import NumberReview
from models.number import TelephoneNumber


class NTPhoneDataParser:

    @staticmethod
    def _weeks_str_to_datetime(weeks_string) -> date:
        weeks = int(weeks_string.split(" ", 1)[0])
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
    def _check_if_actual(reviews: [NumberReview]) -> bool:
        today_date = date.today()
        for review in reviews:
            if (today_date - review.publish_date) < timedelta(days=90):
                return True
        return False

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

        for review_raw in reviews_raw:

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
                    raise InvalidDocumentStructureError(soup.text)

            if author_found := review_raw.find("span", {"itemprop": "author"}):
                author = author_found.text.strip()
            else:
                raise InvalidDocumentStructureError(soup.text)

            if title_found := review_raw.find("span", {"itemprop": "name"}):
                title = title_found.text.strip()
            else:
                raise InvalidDocumentStructureError(soup.text)

            if body_found := review_raw.find("span", class_="review_comment"):
                body = body_found.text.strip()
            else:
                raise InvalidDocumentStructureError(soup.text)

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
        is_actual = NTPhoneDataParser._check_if_actual(reviews)

        return TelephoneNumber(overall_rating, is_actual, number_info, reviews)
