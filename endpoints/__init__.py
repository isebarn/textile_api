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

oid = api.model("oid", {"$oid": String})
base = api.model("base", {"_cls": String, "_id": Nested(oid)})

feature = api.clone(
    "Feature",
    base,
    {
        "feature": String,
        "details": String,
    },
)

variant = api.clone(
    "Variant",
    base,
    {
        "name": String,
        "item_description_line_1": String,
        "item_description_line_2": String,
        "features": List(Nested(feature)),
    },
)

image = api.clone(
    "Image",
    base,
    {
        "url": String,
        "caption": String,
    },
)

product = api.clone(
    "Product",
    base,
    {
        "name": String,
        "detail": String,
        "variants": List(Nested(variant)),
        "images": List(Nested(image)),
    },
)

inquiry = api.clone(
    "Inquiry",
    base,
    {
        "name": String,
        "email": String,
        "phone_number": String,
        "company_name": String,
        "job_title": String,
        "location": String,
        "details": String,
        "status": String,
        "created_on": DateTime(
            attribute=lambda x: datetime.fromtimestamp(
                x.get("created_on", {}).get("$date", 0) / 1e3
            )
        ),
    },
)


@api.route("/features")
class FeaturesController(Resource):
    @api.marshal_list_with(feature)
    def get(self):
        return models.Feature.get(**request.args.to_dict())

    @api.marshal_with(feature)
    def post(self):
        return models.Feature(**request.get_json()).to_json()

    @api.marshal_with(feature)
    def patch(self):
        return models.Feature.set(**request.get_json()).to_json()

    def delete(self):
        models.Feature.objects(id=request.args.get("_id")).delete()


@api.route("/variants")
class VariantsController(Resource):
    @api.marshal_list_with(variant)
    def get(self):
        return models.Variant.get(**request.args.to_dict())

    @api.marshal_with(variant)
    def post(self):
        return models.Variant(**request.get_json()).to_json()

    @api.marshal_with(variant)
    def patch(self):
        return models.Variant.set(**request.get_json()).to_json()

    def delete(self):
        models.Variant.objects(id=request.args.get("_id")).delete()


@api.route("/images")
class ImagesController(Resource):
    @api.marshal_list_with(image)
    def get(self):
        return models.Image.get(**request.args.to_dict())

    @api.marshal_with(image)
    def post(self):
        return models.Image(**request.get_json()).to_json()

    @api.marshal_with(image)
    def patch(self):
        return models.Image.set(**request.get_json()).to_json()

    def delete(self):
        models.Image.objects(id=request.args.get("_id")).delete()


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

    def delete(self):
        models.Product.objects(id=request.args.get("_id")).delete()


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

    def delete(self):
        models.Inquiry.objects(id=request.args.get("_id")).delete()
