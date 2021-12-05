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


@api.route("/")
class ProductsController(Resource):
    def get(self):
        products = models.Product.get()
        product_variants = models.ProductVariant.get()
        product_variant_features = models.ProductVariantFeature.get()

        for product in products:
            product["product_variants"] = []

        for product_variant in product_variants:
            product_variant["product_variant_features"] = []

        for pvf in product_variant_features:
            product_variant_id = (
                pvf.get("product_variant", {}).get("_id", {}).get("$oid")
            )

            if not product_variant_id:
                continue

            product_variant = next(
                filter(
                    lambda x: x["_id"]["$oid"] == product_variant_id, product_variants
                ),
                None,
            )

            if not product_variant:
                continue

            pvf.pop("product_variant")
            product_variant["product_variant_features"].append(pvf)

        for product_variant in product_variants:
            product_id = product_variant.get("product", {}).get("_id", {}).get("$oid")
            if not product_id:
                continue

            product = next(
                filter(lambda x: x["_id"]["$oid"] == product_id, products), None
            )
            if not product:
                continue

            product_variant.pop("product")
            product["product_variants"].append(product_variant)

        return products
