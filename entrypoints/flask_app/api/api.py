import json
from flask import Blueprint, jsonify
from flask_login import login_required
from werkzeug.exceptions import InternalServerError

from service_layer import services
from service_layer import unit_of_work


api = Blueprint('phone-app-api', __name__)


@api.errorhandler(InternalServerError)
def internal_error(error):
    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description
    })
    response.content_type = "application/json"
    return response


@api.route('/api/number/<string:num>')
@login_required
def number_info(num: str):
    try:
        requested_num = services.get_number(digits=num, uow=unit_of_work.SqlalchemyUnitOfWork())
    except services.FailedToLoadPhoneNumberError:
        return jsonify(is_success=False, error_message=f"Phone Info Not Found"), 404
    return jsonify(is_success=True, number_description=requested_num)