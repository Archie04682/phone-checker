from datetime import date
from dataclasses import dataclass

# root: div.review
#   rating: div.score meta(itemprop="ratingValue")
#   tags: div.rightFloat span.reviewTag
#   publish_date: div.rightFloat time(itemprop="datePublished", datetime="2017-05-07 12:45:42")
#   is_precise: div.rightFloat span.review_time.text (true if found)
#   author: h3 span.reviewer span(itemprop="author")
#   title: h3 span(itemprop="name")
#   body: span.review_comment


@dataclass(frozen=True)
class ReviewTag:
    value: str

    def __repr__(self):
        return self.value


class PhoneNumberReview:
    def __init__(
            self,
            rating: float,
            tags: [ReviewTag],
            publish_date: date,
            author: str,
            title: str,
            body: str,
            source: str = ""):

        self.rating = rating
        self.tags = tags
        self.publish_date = publish_date
        self.author = author
        self.title = title
        self.body = body
        self.source = source

    # To and From Dict conversions support:

    class __Fields:
        rating = "rating"
        tags = "tags"
        publish_date = "publish_date"
        author = "author"
        title = "title"
        body = "body"
        source = "source"

    def as_dict(self) -> {}:
        return {
            PhoneNumberReview.__Fields.rating: self.rating,
            PhoneNumberReview.__Fields.tags: [str(tag) for tag in self.tags],
            PhoneNumberReview.__Fields.publish_date: self.publish_date.isoformat(),
            PhoneNumberReview.__Fields.author: self.author,
            PhoneNumberReview.__Fields.title: self.title,
            PhoneNumberReview.__Fields.body: self.body,
            PhoneNumberReview.__Fields.source: self.source
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return PhoneNumberReview(
            rating=dictionary[PhoneNumberReview.__Fields.rating],
            tags=[ReviewTag(tag_str) for tag_str in dictionary[PhoneNumberReview.__Fields.tags]],
            publish_date=date.fromisoformat(dictionary[PhoneNumberReview.__Fields.publish_date]),
            author=dictionary[PhoneNumberReview.__Fields.author],
            title=dictionary[PhoneNumberReview.__Fields.title],
            body=dictionary[PhoneNumberReview.__Fields.body],
            source=dictionary[PhoneNumberReview.__Fields.source]
        )


# There also might be folded commentaries, but it's not necessary for now.
