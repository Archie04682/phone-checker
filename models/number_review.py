from datetime import datetime


class NumberReview:
    def __init__(
            self,
            rating: int,
            tags: [],  # string list
            publish_date: datetime,
            publish_date_is_precise: bool,
            author: str,
            title: str,
            body: str):

        # root: div.review
        self.rating = rating  # div.score meta(itemprop="ratingValue")
        self.tags = tags  # div.rightFloat span.reviewTag
        self.publish_date = publish_date  # div.rightFloat time(itemprop="datePublished", datetime="2017-05-07 12:45:42")
        self.publish_date_is_precise = publish_date_is_precise  # div.rightFloat span.review_time.text to find approx comment date
        self.author = author  # h3 span.reviewer span(itemprop="author")
        self.title = title  # h3 span(itemprop="name")
        self.body = body  # span.review_comment


# There also might be folded commentaries, but it's not necessary for now.
