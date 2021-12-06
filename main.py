# Standard library imports
import os

# Third party imports
from flask import Flask
from flask_restx import Api


# Local application imports
from endpoints import api as _api
from endpoints.products import api as products_api

from flask_cors import CORS

app = Flask("api")
CORS(app, support_credentials=True)

api = Api(app)
api.add_namespace(_api)
api.add_namespace(products_api)
