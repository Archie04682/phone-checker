from datetime import date, timedelta
from typing import Optional

from domain.model.phone_number_review import PhoneNumberReview


class PhoneNumber:
    def __init__(self,
                 rating: float,
                 digits: str,
                 categories: [str],
                 description: Optional[str],
                 reviews: [PhoneNumberReview]):
        self.rating = rating
        self.digits = digits
        self.categories = categories
        self.description = description
        self.reviews = reviews

    @property
    def ref(self):
        return self.digits

    @property
    def is_actual(self) -> bool:
        return len(self.actual_reviews) > 0

    @property
    def actual_reviews(self) -> [PhoneNumberReview]:
        return list(filter(
            lambda rev: (date.today() - rev.publish_date) < timedelta(days=30),
            self.reviews
        ))

    @property
    def old_reviews(self) -> [PhoneNumberReview]:
        return list(filter(
            lambda rev: (date.today() - rev.publish_date) >= timedelta(days=30),
            self.reviews
        ))

    # To and From Dict conversions support:

    class __Fields:
        rating = "rating"
        digits = "digits"
        categories = "categories"
        description = "description"
        reviews = "reviews"

    def as_dict(self):
        return {
            PhoneNumber.__Fields.rating: self.rating,
            PhoneNumber.__Fields.digits: self.digits,
            PhoneNumber.__Fields.categories: self.categories,
            PhoneNumber.__Fields.description: self.description,
            PhoneNumber.__Fields.reviews: [review.as_dict() for review in self.reviews]
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return PhoneNumber(
            rating=dictionary[PhoneNumber.__Fields.rating],
            digits=dictionary[PhoneNumber.__Fields.digits],
            categories=dictionary[PhoneNumber.__Fields.categories],
            description=dictionary[PhoneNumber.__Fields.description],
            reviews=[PhoneNumberReview.from_dict(nr_dict) for nr_dict in dictionary[PhoneNumber.__Fields.reviews]]
        )
