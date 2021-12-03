# Standard library imports
import os
from datetime import datetime

# Third party imports
from flask import Flask
from flask import request
from flask_restx import Namespace
from flask_restx import Resource
from flask_restx import Api
from flask_restx.fields import DateTime
from flask_restx.fields import Float
from flask_restx.fields import List
from flask_restx.fields import Nested
from flask_restx.fields import String
from flask_restx.fields import Boolean
from flask_restx.fields import Raw

# Local application imports
import models

app = Flask(__name__)
api = Api(app)

api = Namespace("api", description="")

oid = api.model("oid", { "$oid": String})
base = api.model("base", {
    "_cls": String,
    "_id": Nested(oid)
})

inquiry = api.clone('Inquiry', base, {
    'name': String,
    'email': String,
    'phone_number': String,
    'company_name': String,
    'job_title': String,
    'location': String,
})

product = api.clone('Product', base, {
    'detail': Raw(),
    'pricing': Raw(),
})



@api.route("/inquiries")
class InquiriesController(Resource):

    @api.marshal_list_with(inquiry)
    def get(self):
        return models.Inquiry.get(**request.args.to_dict())

    @api.marshal_with(inquiry)
    def post(self):
        return models.Inquiry(**request.get_json()).to_json()

    @api.marshal_with(inquiry)
    def patch(self):
        return models.Inquiry.set(**request.get_json()).to_json()

@api.route("/products")
class ProductsController(Resource):

    @api.marshal_list_with(product)
    def get(self):
        return models.Product.get(**request.args.to_dict())

    @api.marshal_with(product)
    def post(self):
        return models.Product(**request.get_json()).to_json()

    @api.marshal_with(product)
    def patch(self):
        return models.Product.set(**request.get_json()).to_json()

