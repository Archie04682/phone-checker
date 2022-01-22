from domain.model import PhoneNumberReview
from tests.random_generators import random_review


def test_can_convert_to_dict():
    review, expected_dict = random_review()
    actual_dict = review.as_dict()
    assert expected_dict == actual_dict


def test_can_construct_from_dict():
    expected_review, initial_dict = random_review()
    actual_review = PhoneNumberReview.from_dict(initial_dict)
    assert expected_review == actual_review
