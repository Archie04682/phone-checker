from datetime import date, timedelta
from domain.model.number_info import NumberInfo
from domain.model.number_review import NumberReview


class _Fields:
    overall_rating = "overall_rating"
    is_actual = "is_actual"
    info = "info"
    reviews = "reviews"


class TelephoneNumber:
    def __init__(self,
                 overall_rating: float,
                 info: NumberInfo,
                 reviews: [NumberReview]):
        self.overall_rating = overall_rating
        self.info = info
        self.reviews = reviews

    @property
    def is_actual(self) -> bool:
        return len(self.actual_reviews) > 0

    @property
    def actual_reviews(self) -> [NumberReview]:
        return list(filter(
            lambda rev: (date.today() - rev.publish_date) < timedelta(days=30),
            self.reviews
        ))

    @property
    def old_reviews(self) -> [NumberReview]:
        return list(filter(
            lambda rev: (date.today() - rev.publish_date) >= timedelta(days=30),
            self.reviews
        ))

    def as_dict(self):
        return {
            _Fields.overall_rating: self.overall_rating,
            _Fields.info: self.info.as_dict(),
            _Fields.reviews: [review.as_dict() for review in self.reviews]
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return TelephoneNumber(
            overall_rating=dictionary[_Fields.overall_rating],
            info=NumberInfo.from_dict(dictionary[_Fields.info]),
            reviews=[NumberReview.from_dict(nr_dict) for nr_dict in dictionary[_Fields.reviews]]
        )
