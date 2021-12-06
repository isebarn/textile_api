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

api = Namespace("products", description="")

oid = api.model("base", {"_id": String(attribute=lambda x: str(x["_id"]))})

product_variant_feature = api.clone(
    "product_variant_feature",
    oid,
    {
        "feature": String,
        "details": String,
    },
)

product_variant = api.clone(
    "product_variant",
    oid,
    {
        "item_description_line_1": String,
        "item_description_line_2": String,
        "name": String,
        "product_variant_features": List(
            Nested(api.models.get("product_variant_feature"))
        ),
    },
)

image = api.clone(
    "image",
    oid,
    {
        "url": String,
        "caption": String,
    },
)

product = api.clone(
    "Product",
    oid,
    {
        "name": String,
        "detail": String,
        "product_variants": List(Nested(api.models.get("product_variant"))),
        "image": List(Nested(api.models.get("image"))),
    },
)


@api.route("/")
class ProductsController(Resource):
    @api.marshal_list_with(product)
    def get(self):
        return list(
            models.Product.objects.aggregate(
                [
                    {
                        "$lookup": {
                            "as": "product_variants",
                            "foreignField": "product",
                            "from": "product_variant",
                            "localField": "_id",
                        }
                    },
                    {"$unwind": "$product_variants"},
                    {
                        "$lookup": {
                            "as": "product_variants.product_variant_features",
                            "foreignField": "product_variant",
                            "from": "product_variant_feature",
                            "localField": "product_variants._id",
                        }
                    },
                    {"$sort": {"product_variants.item_description_line_1": 1}},
                    {
                        "$lookup": {
                            "as": "image",
                            "foreignField": "product",
                            "from": "image",
                            "localField": "_id",
                        }
                    },
                    {"$sort": {"product_variants.product_variant_features._id": 1}},
                    {
                        "$group": {
                            "_id": "$_id",
                            "detail": {"$first": "$detail"},
                            "image": {"$first": "$image"},
                            "name": {"$first": "$name"},
                            "product_variants": {"$push": "$product_variants"},
                        }
                    },
                    {"$sort": {"_id": 1}}
                ]
            )
        )
