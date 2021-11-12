from models.number_info import NumberInfo
from models.number_review import NumberReview


class TelephoneNumber:
    def __init__(self, info: NumberInfo, reviews: [NumberReview]):
        self.info = info
        self.reviews = reviews
