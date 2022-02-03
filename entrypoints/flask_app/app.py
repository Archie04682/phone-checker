from flask import Flask
from flask_bootstrap import Bootstrap

from utils import auth, log
from adapters import orm
from config import FLASK_SECRET_KEY
from entrypoints.flask_web.blueprints.web import web
from entrypoints.flask_web.blueprints.api import api


# Setting up Flask App:
app = Flask(__name__)
app.register_blueprint(web.web)
app.register_blueprint(api.api)
app.config['JSON_AS_ASCII'] = False
app.secret_key = FLASK_SECRET_KEY
Bootstrap(app)
auth.init_app_auth(app)
orm.start_mappers()
orm.create_tables()
logger = log.get_logger()


if __name__ == '__main__':
    logger.info("Flask Web Service started!")
    app.run(debug=True)
