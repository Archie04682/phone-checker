import os
import json
from flask import Flask, jsonify, render_template, redirect, url_for
from flask_login import login_required
from flask_bootstrap import Bootstrap
from werkzeug.exceptions import InternalServerError

from utils import auth, log
from entrypoints.flask_web.forms import PhoneNumberForm, EmailForm
from service_layer import services, unit_of_work
from adapters import orm
from domain.model import PhoneNumber


# Setting up Flask App:
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
Bootstrap(app)
auth.init_app_auth(app)
orm.start_mappers()
logger = log.get_logger()


@app.errorhandler(InternalServerError)
def internal_error(error):
    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description
    })
    response.content_type = "application/json"
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    phone_form = PhoneNumberForm()
    email_form = EmailForm()

    if phone_form.validate_on_submit():
        return redirect(url_for('number', num=phone_form.phone_number.data))

    return render_template('index.html', phoneForm=phone_form, emailForm=email_form)


@app.route('/number/<string:num>')
def number(num: str):
    requested_num = services.get_number(
        digits=num,
        uow=unit_of_work.SqlalchemyUnitOfWork()
    )
    if not requested_num:
        return render_template('not_found.html', phoneNumber=num)
    return render_template('number.html', phoneNumber=PhoneNumber.from_dict(requested_num))


@app.route('/subscribe/<string:email>')
def subscribe(email: str):
    email_form = EmailForm()
    if email_form.validate_on_submit():
        # TODO: Handle subscription here
        print(f"Subscribed: {email}")
    redirect('index.html')


@app.route('/api/number/<string:num>')
@login_required
def number_info(num: str):
    requested_num = services.get_number(
        digits=num,
        uow=unit_of_work.SqlalchemyUnitOfWork()
    )
    if not requested_num:
        return jsonify(is_success=False, error_message=f"Phone Info Not Found"), 404
    return jsonify(is_success=True, number_description=requested_num)


if __name__ == '__main__':
    logger.info("Service started!")
    app.run(debug=True)
