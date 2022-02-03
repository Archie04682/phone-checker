from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email

from utils.number_formatter import NumberFormatter
from phonenumbers import NumberParseException


def validate_phone_number(_, field):
    try:
        normalized_number = NumberFormatter.format(field.data)
    except NumberParseException:
        raise ValidationError('Номер телефона имеет неверный формат')
    else:
        field.data = normalized_number


class PhoneNumberForm(FlaskForm):
    phone_number = StringField('phone-field',
                               validators=[DataRequired("Поле не должно быть пустым"),
                                           validate_phone_number])
    submit = SubmitField('Проверить')


class EmailForm(FlaskForm):
    email = EmailField("Email-адрес:", validators=[Email("Неверный формат email")])
    submit = SubmitField("Отправить")
