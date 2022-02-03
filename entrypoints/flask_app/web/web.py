from flask import Blueprint, redirect, render_template, url_for
from werkzeug.exceptions import InternalServerError

from service_layer import services, unit_of_work
from entrypoints.flask_app.web import forms
from domain import model

web = Blueprint(
    'phone-web-app',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/static/web-app")


@web.errorhandler(InternalServerError)
def internal_error(_):
    return render_template("server_error.html")


@web.route('/', methods=['GET', 'POST'])
def index():
    phone_form = forms.PhoneNumberForm()
    email_form = forms.EmailForm()
    print(web.template_folder)
    print(web.static_folder)
    if phone_form.validate_on_submit():
        return redirect(url_for('phone-web-app.number', num=phone_form.phone_number.data))

    return render_template('index.html', phoneForm=phone_form, emailForm=email_form)


@web.route('/number/<string:num>')
def number(num: str):
    try:
        requested_num = services.get_number(digits=num, uow=unit_of_work.SqlalchemyUnitOfWork())
    except services.FailedToLoadPhoneNumberError:
        return render_template('not_found.html', phoneNumber=num)
    return render_template('number.html', phoneNumber=requested_num)


@web.route('/subscribe/<string:email>', methods=['POST'])
def subscribe(email: str):
    email_form = forms.EmailForm()
    if email_form.validate_on_submit():
        # TODO: Handle subscription here
        print(f"Subscribed: {email}")
    redirect(url_for('phone-web-app.index'))
