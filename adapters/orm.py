from sqlalchemy import Table, Column, DateTime, String, JSON, Integer, Float, ForeignKey
from sqlalchemy.orm import registry, relationship

from domain.model.phone_number import PhoneNumber, NumberCategory
from domain.model.phone_number_review import PhoneNumberReview, ReviewTag


mapper_registry = registry()

review_tags = Table(
    "review_tags",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("review_id", Integer, ForeignKey("reviews.id")),
    Column("value", String, nullable=False)
)

reviews = Table(
    "reviews",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("number_id", Integer, ForeignKey("phone_numbers.id")),
    Column("rating", Float, nullable=False),
    Column("publish_date", DateTime, nullable=False),
    Column("author", String, nullable=False),
    Column("title", String, nullable=False),
    Column("body", String, nullable=False),
    Column("source", String, nullable=False)
)

categories = Table(
    "number_categories",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("number_id", Integer, ForeignKey("phone_numbers.id")),
    Column("value", String, nullable=False)
)

phone_numbers = Table(
    "phone_numbers",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("timestamp", DateTime, nullable=False),
    Column("digits", String(100), nullable=False),
    Column("details", JSON, nullable=False)
)


def start_mappers():
    mapper_registry.map_imperatively(ReviewTag, review_tags)

    mapper_registry.map_imperatively(
        PhoneNumberReview,
        reviews,
        properties={
            "tags": relationship(ReviewTag)
        }
    )

    mapper_registry.map_imperatively(NumberCategory, categories)

    mapper_registry.map_imperatively(
        PhoneNumber,
        phone_numbers,
        properties={
            "categories": relationship(NumberCategory),
            "reviews": relationship(PhoneNumberReview)
        }
    )
