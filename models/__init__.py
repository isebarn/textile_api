# Standard library imports
from json import loads
from json import load
import os
from pprint import pformat
from datetime import datetime

# Third party imports
from bson import json_util
from bson.objectid import ObjectId
from mongoengine import connect
from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import FloatField
from mongoengine import BooleanField
from mongoengine import ReferenceField
from mongoengine import ListField
from mongoengine import StringField
from mongoengine import DictField
from mongoengine import signals

user = os.environ.get("DB_USER", "")
password = os.environ.get("DB_PWD", "")
host = os.environ.get("DB_HOST") or "mongodb+srv://{}".format(host)
database_name = os.environ.get("DB_NAME", "")
db = connect(
    database_name,
    username=user,
    password=password,
    host=host,
    authentication_source="admin",
)


class Extended(Document):
    meta = {"abstract": True, "allow_inheritance": True}

    def __init__(self, *args, **kwargs):
        if "id" in kwargs:
            super(Document, self).__init__(*args, **kwargs)

        else:  # Create new document and recursively create or link to existing ReferenceField docs
            super(Document, self).__init__(
                *args, **{k: v for k, v in kwargs.items() if not isinstance(v, dict)}
            )
            for key, value in self._fields.items():
                if isinstance(value, ReferenceField) and key in kwargs:
                    # link to existing
                    if isinstance(kwargs[key], Document):
                        setattr(self, key, kwargs[key])

                    # pass entire object
                    elif "_id" in kwargs[key]:
                        setattr(
                            self,
                            key,
                            value.document_type_obj.objects.get(id=kwargs[key]["_id"]),
                        )

                    # pass ObjectId string of object
                    elif ObjectId.is_valid(kwargs.get(key, "")):
                        setattr(
                            self,
                            key,
                            value.document_type_obj.objects.get(id=kwargs[key]),
                        )

                    # create new ReferenceField
                    else:
                        setattr(
                            self,
                            key,
                            value.document_type_obj(**{key: {"_id": kwargs[key]}}),
                        )

                # special for Raw fields that are wildcards
                elif isinstance(value, DictField) and isinstance(kwargs.get(key), dict):
                    setattr(self, key, kwargs.get(key))

            self.save()

    def to_json(self):

        return {
            **loads(json_util.dumps(self.to_mongo())),
            **{
                key: getattr(self, key).to_json()
                for key, value in self._fields.items()
                if isinstance(value, ReferenceField) and getattr(self, key)
            },
            **{
                key: [x.to_json() for x in getattr(self, key)]
                for key, value in self._fields.items()
                if isinstance(value, ListField) and getattr(self, key)
            },
        }

    @classmethod
    def set(cls, *args, **kwargs):
        _id = kwargs.pop("_id")
        item = cls.objects.get(id=_id["$oid"])
        for key, value in kwargs.items():
            if isinstance(value, list) and any(value):
                string_object_ids = [x.get("_id", {}).get("$oid") for x in value]
                if all(map(lambda x: ObjectId.is_valid(x), string_object_ids)):
                    value = [ObjectId(x) for x in string_object_ids]

            setattr(item, key, value)

        item.save()

        return cls.objects.get(id=_id["$oid"])

    @classmethod
    def get(cls, *args, **kwargs):
        def recursively_query(model, fields, search, root=False):
            if "___" not in fields:
                if root:
                    field = fields.split("__")[0]
                    if isinstance(getattr(cls, field), DateTimeField):
                        return {fields: datetime.fromisoformat(search)}
                    return {fields: search}

                return [x.id for x in model.objects(**{fields: search})]

            prop, fields = fields.split("___", 1)
            result = recursively_query(
                model._fields[prop].document_type_obj, fields, search
            )

            if not root:
                return [x.id for x in model.objects(**{"{}__in".format(prop): result})]
            else:
                return {"{}__in".format(prop): result}

        filters = {}
        for query, search in kwargs.items():
            filters.update(recursively_query(cls, query, search, True))

        return [x.to_json() for x in cls.objects(**filters)]

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        if kwargs.get("created"):
            pass

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if (
            document.to_json().get("_id")
            and next(cls.objects(id=document.id)).status is not document.status
        ):
            pass


class Feature(Extended):
    feature = StringField()
    details = StringField()


class Variant(Extended):
    name = StringField()
    item_description_line_1 = StringField()
    item_description_line_2 = StringField()
    features = ListField(ReferenceField(Feature, reverse_delete_rule=4))


class Image(Extended):
    url = StringField()
    caption = StringField()


class Product(Extended):
    name = StringField()
    detail = StringField()
    variants = ListField(ReferenceField(Variant, reverse_delete_rule=4))
    images = ListField(ReferenceField(Image, reverse_delete_rule=4))


class Inquiry(Extended):
    name = StringField()
    email = StringField()
    phone_number = StringField()
    company_name = StringField()
    job_title = StringField()
    location = StringField()
    details = StringField()
    status = StringField()
    created_on = DateTimeField(default=datetime.now)


# def config():
# signals.pre_save.connect(Class.pre_save, sender=Class)
# signals.post_save.connect(Class.post_save, sender=Class)

# seed
# logging.info("Seeding database")
# seed = load(open("models/seed.json"))

# helper method to remove "_id" and "_cls" so I can compare json objects
# from the db
# def remove_meta_from_dict_item(item):
#     item.pop("_cls")
#     item.pop("_id")
#     for key, value in item.items():
#         if isinstance(value, dict):
#             remove_meta_from_dict_item(value)


# config()
