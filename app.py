import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from adapters.invalid_document_structure_error import InvalidDocumentStructureError
from services.number_description_service import NumberDescriptionService
from adapters.neberitrubku.nt_phone_data_source import NTPhoneDataSource

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB


class NumberReviewORM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_id = db.Column(db.Integer, db.ForeignKey('number.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(250))
    publish_date = db.Column(db.DateTime, nullable=False)
    precise_date = db.Column(db.Boolean, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    body = db.Column(db.String(250), nullable=False)


class NumberInfoORM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_id = db.Column(db.Integer, db.ForeignKey('number.id'), nullable=False)
    digits = db.Column(db.String(250), nullable=False)
    meta_info = db.Column(db.String(250))
    ratings = db.Column(db.String(250))
    categories = db.Column(db.String(250))
    description = db.Column(db.String(250), nullable=False)


class NumberORM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    overall_rating = db.Column(db.Float, nullable=False)
    is_actual = db.Column(db.Boolean, nullable=False)
    info = db.relationship('NumberInfoORM', backref='number', lazy=True, uselist=False)
    reviews = db.relationship('NumberReviewORM', backref='number', lazy=True)


# DB

nd_service = NumberDescriptionService([NTPhoneDataSource()])


@app.route('/describe/<string:number>')
def describe(number: str):
    try:
        description = nd_service.describe(number)
    except InvalidDocumentStructureError as err:
        return jsonify(is_success=False, error_message=f"Failed To Process Request: {err.message}"), 500

    # TODO: Fix except blocks if there are any errors:

    # except:
    #     return jsonify(is_success=False, error_message=f"Failed To Process Request: unknown reason"), 500

    return jsonify(is_success=True, number_description=description.as_dict())


if __name__ == '__main__':
    app.run(debug=True)

# TODO: Deal with error propagation and logging!
