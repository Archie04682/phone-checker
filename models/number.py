from models.number_info import NumberInfo
from models.number_review import NumberReview


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
            "overall_rating": self.overall_rating,
            "is_actual": self.is_actual,
            "info": self.info.as_dict(),
            "reviews": [review.as_dict() for review in self.reviews]
        }
