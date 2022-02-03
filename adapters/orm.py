from sqlalchemy import Table, Column, Date, String, Integer, Float, ForeignKey, create_engine
from sqlalchemy.orm import registry, relationship

from domain.model import PhoneNumber, NumberCategory
from domain.model import PhoneNumberReview, ReviewTag
from config import get_postgres_uri


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
    Column("publish_date", Date, nullable=False),
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
    Column("rating", Float, nullable=False),
    Column("digits", String(100), nullable=False),
    Column("description", String),
    Column("timestamp", Date, nullable=False)
)


def start_mappers():
    mapper_registry.map_imperatively(ReviewTag, review_tags)

    mapper_registry.map_imperatively(
        PhoneNumberReview,
        reviews,
        properties={
            "tags": relationship(ReviewTag, lazy="joined", cascade="all, expunge")
        }
    )

    mapper_registry.map_imperatively(NumberCategory, categories)

    mapper_registry.map_imperatively(
        PhoneNumber,
        phone_numbers,
        properties={
            "categories": relationship(NumberCategory, lazy="joined", cascade="all, expunge"),
            "reviews": relationship(PhoneNumberReview, lazy="joined", cascade="all, expunge")
        }
    )


def create_tables():
    engine = create_engine(get_postgres_uri())
    mapper_registry.metadata.create_all(engine)
