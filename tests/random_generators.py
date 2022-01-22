import uuid
from random import randint, uniform, choice
from datetime import date, timedelta
from domain.model import PhoneNumber, NumberCategory, PhoneNumberReview, ReviewTag

# Generic Types:


def random_str(length: int = 8) -> str:
    val = uuid.uuid4().hex
    if length < 1 or length > len(val):
        return val
    return val[:length]


def random_int(lower: int = 1, upper: int = 5) -> int:
    return randint(lower, upper)


def random_float(lower: float = 0.0, upper: float = 5.0) -> float:
    return uniform(lower, upper)


def random_date() -> date:
    return date.today() - timedelta(days=random_int(0, 180))


def random_digits() -> str:
    random_part = ''.join([str(random_int(0, 9)) for _ in range(0, 7)])
    return f"7800{random_part}"


# Review Tag:


def random_review_tag() -> (ReviewTag, str):
    val = f"tag-{random_str()}"
    return ReviewTag(value=val), val


def random_review_tags() -> [(ReviewTag, str)]:
    return [random_review_tag() for _ in range(0, random_int())]


# Phone Number Review:


def random_review() -> (PhoneNumberReview, dict):
    rating = random_float()
    tags, tag_values = map(list, zip(*random_review_tags()))
    publish_date = random_date()
    author = f"author-{random_str()}"
    title = f"title-{random_str()}"
    body = f"body-{random_str()}"
    source = f"source-{random_str()}"

    review_dict = {
        "rating": rating,
        "tags": tag_values,
        "publish_date": publish_date.isoformat(),
        "author": author,
        "title": title,
        "body": body,
        "source": source
    }

    review_obj = PhoneNumberReview(
        rating=rating,
        tags=tags,
        publish_date=publish_date,
        author=author,
        title=title,
        body=body,
        source=source
    )

    return review_obj, review_dict


def random_reviews() -> [(PhoneNumberReview, dict)]:
    return [random_review() for _ in range(0, random_int())]


# Phone Number Category:


def random_number_category() -> (NumberCategory, str):
    val = f"category-{random_str()}"
    return NumberCategory(value=val), val


def random_number_categories() -> [(NumberCategory, str)]:
    return [random_number_category() for _ in range(0, random_int())]


# Phone Number:


def random_phone_number() -> (PhoneNumber, dict):
    rating = random_float()
    digits = random_digits()
    categories, category_values = map(list, zip(*random_number_categories()))
    description = choice([f"description-{random_str()}", None])
    reviews, review_values = map(list, zip(*random_reviews()))
    timestamp = date.today()

    phone_number_dict = {
        "rating": rating,
        "digits": digits,
        "categories": category_values,
        "description": description,
        "reviews": review_values,
        "timestamp": timestamp.isoformat()
    }

    phone_number_obj = PhoneNumber(
        rating=rating,
        digits=digits,
        categories=categories,
        description=description,
        reviews=reviews,
        timestamp=timestamp
    )

    return phone_number_obj, phone_number_dict


def random_phone_numbers(count: int) -> [(PhoneNumber, dict)]:
    if count == 0:
        return [random_phone_number() for _ in range(0, random_int())]
    return [random_phone_number() for _ in range(0, count)]
