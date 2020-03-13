from flask_restplus import fields
from . import api

pagination_model = api.model("Pagination", {
    "page": fields.Integer,
    "pages": fields.Integer,
    "total": fields.Integer,
})
