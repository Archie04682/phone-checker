from datetime import date, timedelta
from tests.random_generators import random_phone_number, random_reviews
from domain.model import PhoneNumber, PhoneNumberReview
from config import REVIEW_ACTUALITY_DELTA


def get_reviews(timedelta_from_today: timedelta) -> [PhoneNumberReview]:
    reviews, _ = map(list, zip(*random_reviews()))
    for review in reviews:
        review.publish_date = date.today() - timedelta_from_today
    return reviews


def prepare_number_and_reviews():
    num, _ = random_phone_number()
    num.reviews = []
    old_reviews = get_reviews(REVIEW_ACTUALITY_DELTA)
    new_reviews = get_reviews(timedelta())
    return num, old_reviews, new_reviews


def test_can_convert_to_dict():
    number, expected_dict = random_phone_number()
    actual_dict = number.as_dict()
    assert expected_dict == actual_dict


def test_can_construct_from_dict():
    expected_number, initial_dict = random_phone_number()
    actual_number = PhoneNumber.from_dict(initial_dict)
    assert expected_number == actual_number


def test_returns_digits_as_ref():
    number, _ = random_phone_number()
    assert number.digits == number.ref


# noinspection DuplicatedCode
def test_can_check_actuality():
    number, old_reviews, new_reviews = prepare_number_and_reviews()

    assert not number.is_actual

    number.reviews = old_reviews
    assert not number.is_actual

    number.reviews = new_reviews
    assert number.is_actual

    number.reviews = old_reviews + new_reviews
    assert number.is_actual


# noinspection DuplicatedCode
def test_filters_out_actual_reviews():
    number, old_reviews, new_reviews = prepare_number_and_reviews()

    assert not number.actual_reviews

    number.reviews = old_reviews
    assert not number.actual_reviews

    number.reviews = new_reviews
    assert number.actual_reviews == new_reviews

    number.reviews = old_reviews + new_reviews
    assert number.actual_reviews == new_reviews


# noinspection DuplicatedCode
def test_filters_out_old_reviews():
    number, old_reviews, new_reviews = prepare_number_and_reviews()

    assert not number.old_reviews

    number.reviews = new_reviews
    assert not number.old_reviews

    number.reviews = old_reviews
    assert number.old_reviews == old_reviews

    number.reviews = old_reviews + new_reviews
    assert number.old_reviews == old_reviews
