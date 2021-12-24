from flask import Flask, jsonify, render_template, redirect, url_for
from flask_login import login_required
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
from os import environ

from adapters.exceptions import InvalidDocumentStructureError, PhoneDataNotFoundError
from adapters.neberitrubku.nt_phone_data_repository import NTPhoneDataSource
from services.number_description_service import NumberDescriptionService
from services.pg.pg_number_cache_service import get_pg_cache_service
from services.logger_provider import get_logger
from services.authorization_service import init_app_auth

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = environ.get('FLASK_SECRET_KEY')
Bootstrap(app)

# Flask-Login setup
init_app_auth(app)

# Manual DI =)
cache_service = get_pg_cache_service(app, timedelta(weeks=2))
logger = get_logger()
nd_service = NumberDescriptionService(cache_service, [NTPhoneDataSource()], logger)

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
    phone_number = StringField('phone-field',
                               validators=[DataRequired("Поле не должно быть пустым"), validate_phone_number])
    submit = SubmitField('Проверить')


class EmailForm(FlaskForm):
    email = EmailField("Email-адрес:", validators=[Email("Неверный формат email")])
    submit = SubmitField("Отправить")


#


@app.route('/', methods=['GET', 'POST'])
def index():
    phone_form = PhoneNumberForm()
    email_form = EmailForm()

    if phone_form.validate_on_submit():
        return redirect(url_for('number', num=phone_form.phone_number.data))

    # if request.method == 'POST':
    #     if phone_form.submit.data and phone_form.validate():
    #         return redirect(url_for('number_info', number=phone_form.phone_number.data))
    #     if email_form.submit.data and email_form.validate():
    #         pass

    return render_template('index.html', phoneForm=phone_form, emailForm=email_form)


@app.route('/number/<string:num>')
def number(num: str):
    try:
        normalized_number = NumberNormalizeService.normalize(num)
        description = nd_service.describe(normalized_number)
    except InvalidDocumentStructureError as err:
        return render_template('server_error.html')
    except PhoneDataNotFoundError as err:
        return render_template('not_found.html', phoneNumber=NumberNormalizeService.prettify(num))

    return render_template('number.html', phoneNumber=description)


@app.route('/subscribe/<string:email>')
def subscribe(email: str):
    email_form = EmailForm()
    if email_form.validate_on_submit():
        pass
    redirect('index.html')


@app.route('/api/number/<string:num>')
@login_required
def number_info(num: str):
    try:
        normalized_number = NumberNormalizeService.normalize(num)
        description = nd_service.describe(normalized_number)
    except InvalidDocumentStructureError as err:
        return jsonify(is_success=False, error_message=f"Failed To Process Request: {err.message}"), 500
    except PhoneDataNotFoundError as err:
        return jsonify(is_success=False, error_message=f"Phone Info Not Found"), 404

    # TODO: Fix except blocks if there are any errors:
    # except:
    #     return jsonify(is_success=False, error_message=f"Failed To Process Request: unknown reason"), 500

    return jsonify(is_success=True, number_description=description.as_dict())


def run_prod():
    app.run()


if __name__ == '__main__':
    logger.info("Service started!")
    app.run(debug=True)

# TODO: Deal with error propagation and logging!
