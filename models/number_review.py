from datetime import datetime

# root: div.review
#   rating: div.score meta(itemprop="ratingValue")
#   tags: div.rightFloat span.reviewTag
#   publish_date: div.rightFloat time(itemprop="datePublished", datetime="2017-05-07 12:45:42")
#   is_precise: div.rightFloat span.review_time.text (true if found)
#   author: h3 span.reviewer span(itemprop="author")
#   title: h3 span(itemprop="name")
#   body: span.review_comment


class NumberReview:
    def __init__(
            self,
            rating: float,
            tags: [str],
            publish_date: datetime,
            publish_date_is_precise: bool,
            author: str,
            title: str, body: str):

        self.rating = rating
        self.tags = tags
        self.publish_date = publish_date
        self.publish_date_is_precise = publish_date_is_precise
        self.author = author
        self.title = title
        self.body = body

    def as_dict(self) -> {}:
        return {
            "rating": self.rating,
            "tags": self.tags,
            "publish_date": self.publish_date.isoformat(),
            "publish_date_is_precise": self.publish_date_is_precise,
            "author": self.author,
            "title": self.title,
            "body": self.body
        }


# There also might be folded commentaries, but it's not necessary for now.
