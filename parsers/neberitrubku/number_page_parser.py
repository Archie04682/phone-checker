from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging

from models.number_info import NumberInfo
from models.number_review import NumberReview
from models.number import TelephoneNumber
from parsers.invalid_document_structure_error import InvalidDocumentStructureError


class NumberPageParser:

    @staticmethod
    def _weeks_str_to_datetime(weeks_string) -> datetime:
        weeks = int(weeks_string.split(" ", 1)[0])
        print(f"subtracted {weeks} weeks...")
        return datetime.today() - timedelta(weeks=weeks)

    @staticmethod
    def _calc_overall_rating(ratings: {int: str}):
        total = 0
        division_factor = 0
        for count, rating_string in ratings.items():
            division_factor += total
            if rating_string == "положительная":
                total += count * 5
            elif rating_string == "отрицательная":
                total += count * 1
            else:
                total += count * 3
                if rating_string != "нейтральная":
                    logging.info(f"Unknown rating string found: '{rating_string}'.")
        return total / division_factor

    @staticmethod
    def _check_if_actual(reviews: [NumberReview]) -> bool:
        today_datetime = datetime.today()
        for review in reviews:
            if (today_datetime - review.publish_date) < timedelta(days=90):
                return True
        return False

    @staticmethod
    def _parse_number_info(soup: BeautifulSoup) -> NumberInfo:

        main_info_div = soup.find("div", class_="mainInfo")

        if digits_found := main_info_div.select_one("div.mainInfoHeader div.number"):
            digits = digits_found.find(text=True, recursive=False).text.strip()
        else:
            raise InvalidDocumentStructureError(soup.text)

        meta_info = [span.text.strip() for span in main_info_div.select("div.mainInfoHeader div.number span")]

        ratings_raw = [rating.text.split('x ') for rating in main_info_div.select("div.description div.ratings li")]
        ratings = {int(rating[0].strip()): rating[-1].strip() for rating in ratings_raw}

        categories_raw = [cat.text.split('x ') for cat in main_info_div.select("div.description div.categories li")]
        categories = {cat[0].strip(): cat[-1].strip() for cat in categories_raw}

        if description_found := main_info_div.select_one("div.description div.advanced div"):
            description = description_found.text.strip()
        else:
            raise InvalidDocumentStructureError(soup.text)

        return NumberInfo(
            digits,
            meta_info,
            ratings,
            categories,
            description
        )

    @staticmethod
    def _parse_number_reviews(soup: BeautifulSoup) -> [NumberReview]:

        reviews_raw = [review
                       for review
                       in soup.find_all("div", class_="review")
                       if "reviewNew" not in review.attrs["class"]]
        reviews = []

        for review_raw in reviews_raw:

            if rating_found := review_raw.find("meta", {"itemprop": "ratingValue"}):
                rating = int(rating_found.attrs["content"])
            else:
                raise InvalidDocumentStructureError(soup.text)

            tags = [tag.text.strip() for tag in review_raw.find_all(class_="reviewTag")]

            publish_date_found = review_raw.find("time", {"itemprop": "datePublished"})
            if publish_date_found:
                publish_date = datetime.fromisoformat(publish_date_found.attrs["datetime"])
                publish_date_is_precise = True
            else:
                publish_date_is_precise = False
                review_time_found = review_raw.find("span", class_="review_time")
                if review_time_found:
                    publish_date = NumberPageParser._weeks_str_to_datetime(review_time_found.text.strip())
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

        number_info = NumberPageParser._parse_number_info(soup)
        reviews = NumberPageParser._parse_number_reviews(soup)
        overall_rating = NumberPageParser._calc_overall_rating(number_info.ratings)
        is_actual = NumberPageParser._check_if_actual(reviews)

        return TelephoneNumber(overall_rating, is_actual, number_info, reviews)
