import os
import logging

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify

from models.number import TelephoneNumber
from services.number_cache_service import NumberCacheService


def get_pg_cache_service(app: Flask, cache_actuality: timedelta):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:qwerty@localhost/phones')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    logging.info(f"Initialized pg-cache with params: {app.config['SQLALCHEMY_DATABASE_URI']}")

    class NumberORM(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        timestamp = db.Column(db.DateTime, nullable=False)
        digits = db.Column(db.String(100), nullable=False)
        details = db.Column(db.JSON, nullable=False)

        @staticmethod
        def generate_from_model(digits: str, model: TelephoneNumber):
            return NumberORM(
                timestamp=datetime.now(),
                digits=digits,
                details=model.as_dict()
            )

        def export_to_model(self) -> TelephoneNumber:
            return TelephoneNumber.from_dict(dict(self.details))

    db.create_all()

    class PGNumberCacheService(NumberCacheService):
        def get(self, digits: str) -> TelephoneNumber or None:
            if found_num := NumberORM.query.filter(NumberORM.digits == digits).first():
                if self.__actuality_delta > (datetime.now() - found_num.timestamp):
                    return found_num.export_to_model()
            return None

        def put(self, digits: str, data: TelephoneNumber):
            if found_num := self.get(digits):
                found_num.timestamp = datetime.now()
                found_num.details = data.as_dict()
            else:
                new_num = NumberORM.generate_from_model(digits, data)
                self.__db.session.add(new_num)
            self.__db.session.commit()

        def __init__(self, database: SQLAlchemy, __actuality_delta: timedelta):
            self.__db = database
            self.__actuality_delta = __actuality_delta

    return PGNumberCacheService(db, cache_actuality)
