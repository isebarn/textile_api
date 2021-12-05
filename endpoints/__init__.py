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
    },
)

product = api.clone(
    "Product",
    base,
    {
        "name": String,
        "detail": String,
    },
)

product_variant = api.clone(
    "Product_variant",
    base,
    {
        "item_description_line_1": String,
        "item_description_line_2": String,
        "product": Nested(product),
    },
)

product_variant_feature = api.clone(
    "Product_variant_feature",
    base,
    {
        "feature": String,
        "details": String,
        "product_variant": Nested(product_variant),
    },
)

image = api.clone(
    "Image",
    base,
    {
        "url": String,
        "caption": String,
        "product": Nested(product),
    },
)


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


@api.route("/product_variants")
class ProductVariantsController(Resource):
    @api.marshal_list_with(product_variant)
    def get(self):
        return models.ProductVariant.get(**request.args.to_dict())

    @api.marshal_with(product_variant)
    def post(self):
        return models.ProductVariant(**request.get_json()).to_json()

    @api.marshal_with(product_variant)
    def patch(self):
        return models.ProductVariant.set(**request.get_json()).to_json()


@api.route("/product_variant_feature")
class ProductVariantFeatureController(Resource):
    @api.marshal_list_with(product_variant_feature)
    def get(self):
        return models.ProductVariantFeature.get(**request.args.to_dict())

    @api.marshal_with(product_variant_feature)
    def post(self):
        return models.ProductVariantFeature(**request.get_json()).to_json()

    @api.marshal_with(product_variant_feature)
    def patch(self):
        return models.ProductVariantFeature.set(**request.get_json()).to_json()


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
