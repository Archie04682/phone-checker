from datetime import date, timedelta
from dateutil import parser
from typing import Optional
from dataclasses import dataclass
from config import REVIEW_ACTUALITY_DELTA


@dataclass(frozen=True, eq=True)
class ReviewTag:
    value: str

    def __repr__(self):
        return self.value


@dataclass(eq=True)
class PhoneNumberReview:
    rating: float
    tags: [ReviewTag]
    publish_date: date
    author: str
    title: str
    body: str
    source: str = ""

    # To and From Dict conversions support:

    def as_dict(self) -> {}:
        return {
            "rating": self.rating,
            "tags": [str(tag) for tag in self.tags],
            "publish_date": self.publish_date.isoformat(),
            "author": self.author,
            "title": self.title,
            "body": self.body,
            "source": self.source
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return PhoneNumberReview(
            rating=dictionary["rating"],
            tags=[ReviewTag(tag_str) for tag_str in dictionary["tags"]],
            publish_date=parser.parse(dictionary["publish_date"]).date(),
            author=dictionary["author"],
            title=dictionary["title"],
            body=dictionary["body"],
            source=dictionary["source"]
        )

    # There also might be folded commentaries, but it's not necessary for now.


@dataclass(eq=True)
class NumberCategory:
    value: str

    def __repr__(self):
        return self.value


# Aggregate Root
# TODO: Add Versioning with implementing modifying functions (such as adding a review)
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

    def __eq__(self, other):
        if not isinstance(other, PhoneNumber):
            return False
        return (self.rating == other.rating
                and self.digits == other.digits
                and self.categories == other.categories
                and self.description == other.description
                and self.reviews == other.reviews
                and self.timestamp == other.timestamp)

    @property
    def ref(self):
        return self.digits

    @property
    def is_actual(self) -> bool:
        return len(self.actual_reviews) > 0

    @property
    def actual_reviews(self) -> [PhoneNumberReview]:
        return list(filter(
            lambda rev: (date.today() - rev.publish_date) < REVIEW_ACTUALITY_DELTA,
            self.reviews
        ))

    @property
    def old_reviews(self) -> [PhoneNumberReview]:
        return list(filter(
            lambda rev: (date.today() - rev.publish_date) >= REVIEW_ACTUALITY_DELTA,
            self.reviews
        ))

    # To and From Dict conversions support:

    def as_dict(self):
        return {
            "rating": self.rating,
            "digits": self.digits,
            "categories": [str(cat) for cat in self.categories],
            "description": self.description,
            "reviews": [review.as_dict() for review in self.reviews],
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return PhoneNumber(
            rating=dictionary["rating"],
            digits=dictionary["digits"],
            categories=[NumberCategory(cat_str) for cat_str in dictionary["categories"]],
            description=dictionary["description"],
            reviews=[PhoneNumberReview.from_dict(nr_dict) for nr_dict in dictionary["reviews"]],
            timestamp=parser.parse(dictionary["timestamp"]).date()
        )
