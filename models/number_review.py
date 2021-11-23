from datetime import datetime

# root: div.review
#   rating: div.score meta(itemprop="ratingValue")
#   tags: div.rightFloat span.reviewTag
#   publish_date: div.rightFloat time(itemprop="datePublished", datetime="2017-05-07 12:45:42")
#   is_precise: div.rightFloat span.review_time.text (true if found)
#   author: h3 span.reviewer span(itemprop="author")
#   title: h3 span(itemprop="name")
#   body: span.review_comment


class _Fields:
    rating = "rating"
    tags = "tags"
    publish_date = "publish_date"
    is_precise = "is_precise"
    author = "author"
    title = "title"
    body = "body"


class NumberReview:
    def __init__(
            self,
            rating: float,
            tags: [str],
            publish_date: datetime,
            is_precise: bool,
            author: str,
            title: str, body: str):

        self.rating = rating
        self.tags = tags
        self.publish_date = publish_date
        self.is_precise = is_precise
        self.author = author
        self.title = title
        self.body = body

    def as_dict(self) -> {}:
        return {
            _Fields.rating: self.rating,
            _Fields.tags: self.tags,
            _Fields.publish_date: self.publish_date.isoformat(),
            _Fields.is_precise: self.is_precise,
            _Fields.author: self.author,
            _Fields.title: self.title,
            _Fields.body: self.body
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return NumberReview(
            rating=dictionary[_Fields.rating],
            tags=dictionary[_Fields.tags],
            publish_date=datetime.fromisoformat(dictionary[_Fields.publish_date]),
            is_precise=dictionary[_Fields.is_precise],
            author=dictionary[_Fields.author],
            title=dictionary[_Fields.title],
            body=dictionary[_Fields.body]
        )


# There also might be folded commentaries, but it's not necessary for now.
