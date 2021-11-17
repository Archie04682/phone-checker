import uuid

from flask import Flask, jsonify, Response
# from flask_sqlalchemy import SQLAlchemy

from adapters.invalid_document_structure_error import InvalidDocumentStructureError
from services.number_description_service import NumberDescriptionService
from adapters.neberitrubku.nt_phone_data_source import NTPhoneDataSource

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
nd_service = NumberDescriptionService([NTPhoneDataSource()])


@app.route('/describe/<string:number>')
def describe(number: str):
    try:
        description = nd_service.describe(number)
    except InvalidDocumentStructureError as err:
        return jsonify(is_success=False, error_message=f"Failed To Process Request: {err.message}"), 500

    #TODO: Fix except blocks if there are any errors:

    # except:
    #     return jsonify(is_success=False, error_message=f"Failed To Process Request: unknown reason"), 500

    return jsonify(is_success=True, number_description=description.as_dict())


if __name__ == '__main__':
    app.run(debug=True)

#TODO: Deal with error propagation and logging!