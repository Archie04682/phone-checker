from flask import Flask, jsonify, render_template, redirect, url_for, request
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import Form, StringField, EmailField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from os import environ

from adapters.exceptions import InvalidDocumentStructureError, PhoneDataNotFoundError
from adapters.neberitrubku.nt_phone_data_source import NTPhoneDataSource
from services.number_description_service import NumberDescriptionService
from services.pg.pg_number_cache_service import get_pg_cache_service
from services.number_normalize_service import NumberNormalizeService
from services.logger_provider import get_logger

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = environ.get('FLASK_SECRET_KEY')
Bootstrap(app)

nd_service = NumberDescriptionService([NTPhoneDataSource()])
cache_service = get_pg_cache_service(app, timedelta(weeks=2))
logger = get_logger()

# WTForms

from services.number_normalize_service import NumberNormalizeService
from phonenumbers import NumberParseException
from wtforms import ValidationError


def validate_phone_number(form, field):
    try:
        normalized_number = NumberNormalizeService.normalize(field.data)
    except NumberParseException:
        raise ValidationError('Номер телефона имеет неверный формат')
    else:
        field.data = normalized_number


class PhoneNumberForm(FlaskForm):
    phone_number = StringField('Номер Телефона', validators=[
        DataRequired("Поле не должно быть пустым"), validate_phone_number
    ])

#


@app.route('/', methods=['GET', 'POST'])
def index():
    phone_form = PhoneNumberForm()
    if phone_form.validate_on_submit():
        return redirect(url_for('describe', number=phone_form.phone_number.data))
    return render_template('index.html', phoneForm=phone_form)


@app.route('/api/number/<string:number>')
def describe(number: str):
    try:
        normalized_number = NumberNormalizeService.normalize(number)

        if cached_description := cache_service.get(normalized_number):
            description = cached_description
            logger.info(f"Retrieved cached version for {number}")
        else:
            description = nd_service.describe(number)
            cache_service.put(normalized_number, description)
            logger.info(f"Requested new version for {number}")

    except InvalidDocumentStructureError as err:
        return jsonify(is_success=False, error_message=f"Failed To Process Request: {err.message}"), 500
    except PhoneDataNotFoundError as err:
        return jsonify(is_success=False, error_message=f"Phone Info Not Found"), 404

    # TODO: Fix except blocks if there are any errors:

    # except:
    #     return jsonify(is_success=False, error_message=f"Failed To Process Request: unknown reason"), 500

    return jsonify(is_success=True, number_description=description.as_dict())


if __name__ == '__main__':
    logger.info("Service started!")
    app.run(debug=True)

# TODO: Deal with error propagation and logging!
