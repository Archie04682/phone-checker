from flask import Flask, jsonify
from datetime import timedelta
import logging

from adapters.invalid_document_structure_error import InvalidDocumentStructureError
from adapters.neberitrubku.nt_phone_data_source import NTPhoneDataSource
from services.number_description_service import NumberDescriptionService
from services.pg.pg_number_cache_service import get_pg_cache_service
from services.number_normalize_service import NumberNormalizeService

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

nd_service = NumberDescriptionService([NTPhoneDataSource()])
cache_service = get_pg_cache_service(app, timedelta(weeks=2))

logger = logging.getLogger('flask-app')
file_handler = logging.FileHandler("flask-app-log.txt")
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)s-%(levelname)s: %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


@app.route('/describe/<string:number>')
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

    # TODO: Fix except blocks if there are any errors:

    # except:
    #     return jsonify(is_success=False, error_message=f"Failed To Process Request: unknown reason"), 500

    return jsonify(is_success=True, number_description=description.as_dict())


if __name__ == '__main__':
    app.run(debug=True)

# TODO: Deal with error propagation and logging!
