from datetime import date, timedelta
from typing import Optional
from dataclasses import dataclass

from domain.model.phone_number_review import PhoneNumberReview


@dataclass(frozen=True)
class NumberCategory:
    value: str

    def __repr__(self):
        return self.value


class PhoneNumber:
    def __init__(self,
                 rating: float,
                 digits: str,
                 categories: [NumberCategory],
                 description: Optional[str],
                 reviews: [PhoneNumberReview],
                 timestamp: date = date.today()):
        self.rating = rating
        self.digits = digits
        self.categories = categories
        self.description = description
        self.reviews = reviews
        self.timestamp = timestamp

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
        timestamp = "timestamp"

    def as_dict(self):
        return {
            PhoneNumber.__Fields.rating: self.rating,
            PhoneNumber.__Fields.digits: self.digits,
            PhoneNumber.__Fields.categories: [str(cat) for cat in self.categories],
            PhoneNumber.__Fields.description: self.description,
            PhoneNumber.__Fields.reviews: [review.as_dict() for review in self.reviews],
            PhoneNumber.__Fields.timestamp: self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return PhoneNumber(
            rating=dictionary[PhoneNumber.__Fields.rating],
            digits=dictionary[PhoneNumber.__Fields.digits],
            categories=[NumberCategory(cat_str) for cat_str in dictionary[PhoneNumber.__Fields.categories]],
            description=dictionary[PhoneNumber.__Fields.description],
            reviews=[PhoneNumberReview.from_dict(nr_dict) for nr_dict in dictionary[PhoneNumber.__Fields.reviews]],
            timestamp=date.fromisoformat(dictionary[PhoneNumber.__Fields.timestamp])
        )
