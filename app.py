import uuid

from flask import Flask, jsonify
# from flask_sqlalchemy import SQLAlchemy
from services.number_description_service import NumberDescriptionService

app = Flask(__name__)
ns_service = NumberDescriptionService()


@app.route('/describe/<string:number>')
def describe(number: str):  # put application's code here
    trace_id = uuid.uuid1().hex

    try:
        description = ns_service.describe(number, trace_id)
    except:
        return jsonify(is_success=False, error_message="Failed To Process Request"), 500

    return jsonify(is_success=True, number_description=description.as_dict())


if __name__ == '__main__':
    app.run(debug=True)

#TODO: Deal with error propagation and logging!