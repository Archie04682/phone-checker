from datetime import date

# root: div.review
#   rating: div.score meta(itemprop="ratingValue")
#   tags: div.rightFloat span.reviewTag
#   publish_date: div.rightFloat time(itemprop="datePublished", datetime="2017-05-07 12:45:42")
#   is_precise: div.rightFloat span.review_time.text (true if found)
#   author: h3 span.reviewer span(itemprop="author")
#   title: h3 span(itemprop="name")
#   body: span.review_comment


class PhoneNumberReview:
    def __init__(
            self,
            rating: float,
            tags: [str],
            publish_date: date,
            is_precise: bool,
            author: str,
            title: str,
            body: str):

        self.rating = rating
        self.tags = tags
        self.publish_date = publish_date
        self.is_precise = is_precise
        self.author = author
        self.title = title
        self.body = body

    # To and From Dict conversions support:

    class __Fields:
        rating = "rating"
        tags = "tags"
        publish_date = "publish_date"
        is_precise = "is_precise"
        author = "author"
        title = "title"
        body = "body"

    def as_dict(self) -> {}:
        return {
            PhoneNumberReview.__Fields.rating: self.rating,
            PhoneNumberReview.__Fields.tags: self.tags,
            PhoneNumberReview.__Fields.publish_date: self.publish_date.isoformat(),
            PhoneNumberReview.__Fields.is_precise: self.is_precise,
            PhoneNumberReview.__Fields.author: self.author,
            PhoneNumberReview.__Fields.title: self.title,
            PhoneNumberReview.__Fields.body: self.body
        }

    @staticmethod
    def from_dict(dictionary: {}):
        return PhoneNumberReview(
            rating=dictionary[PhoneNumberReview.__Fields.rating],
            tags=dictionary[PhoneNumberReview.__Fields.tags],
            publish_date=date.fromisoformat(dictionary[PhoneNumberReview.__Fields.publish_date]),
            is_precise=dictionary[PhoneNumberReview.__Fields.is_precise],
            author=dictionary[PhoneNumberReview.__Fields.author],
            title=dictionary[PhoneNumberReview.__Fields.title],
            body=dictionary[PhoneNumberReview.__Fields.body]
        )


# There also might be folded commentaries, but it's not necessary for now.
