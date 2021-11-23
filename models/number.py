from models.number_info import NumberInfo
from models.number_review import NumberReview


class _Fields:
    overall_rating = "overall_rating"
    is_actual = "is_actual"
    info = "info"
    reviews = "reviews"


class TelephoneNumber:
    def __init__(self,
                 overall_rating: float,
                 is_actual: bool,
                 info: NumberInfo,
                 reviews: [NumberReview]):

        self.overall_rating = overall_rating
        self.is_actual = is_actual
        self.info = info
        self.reviews = reviews

    def as_dict(self):
        return {
            _Fields.overall_rating: self.overall_rating,
            _Fields.is_actual: self.is_actual,
            _Fields.info: self.info.as_dict(),
            _Fields.reviews: [review.as_dict() for review in self.reviews]
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return TelephoneNumber(
            overall_rating=dictionary[_Fields.overall_rating],
            is_actual=dictionary[_Fields.is_actual],
            info=NumberInfo.from_dict(dictionary[_Fields.info]),
            reviews=[NumberReview.from_dict(nr_dict) for nr_dict in dictionary[_Fields.reviews]]
        )
