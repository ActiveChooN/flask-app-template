from flask import jsonify
from flask_restplus import Resource, Namespace, reqparse, fields, inputs, abort
from flask_restplus._http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from application import app, jwt
from .api_models import pagination_model
from .parsers import paging_parser

# Namespace

users_ns = Namespace("Users", description="Users endpoint", path="users")

# Parsers

user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=str, location="json",
                         help="Username of a user")
user_parser.add_argument("password", type=str, location="json",
                         help="Password of a user")
user_parser.add_argument("email", type=inputs.email(), location="json",
                         help="Email of a user")
user_parser.add_argument("name", type=str, location="json",
                         help="First or/and second name of a user")
user_parser.add_argument("is_active", type=bool, location="json", default=True,
                         help="Active or disabled user")
user_parser.add_argument("role", type=str, location="json",
                         help="User role")

post_user_parser = user_parser.copy()
post_user_parser.replace_argument("username", type=str, location="json",
                                  required=True, help="Username of a user")
post_user_parser.replace_argument("password", type=str, location="json",
                                  required=True, help="Password of a user")
post_user_parser.replace_argument("role", type=str, location="json",
                                  required=True, help="User role")

# Models

user_model = users_ns.model("User", {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "name": fields.String,
    "is_active": fields.Boolean,
    "role": fields.String(attribute="role.name")
})

users_model = users_ns.inherit("Users", pagination_model, {
    "users": fields.List(fields.Nested(user_model), attribute="items")
})

# Resources


@users_ns.route("/")
class Users(Resource):
    @jwt_required
    @users_ns.marshal_with(users_model)
    def get(self):
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @jwt_required
    @users_ns.marshal_with(user_model)
    @users_ns.expect(post_user_parser)
    def post(self):
        abort(HTTPStatus.NOT_IMPLEMENTED)


@users_ns.route("/<int:id>")
@users_ns.doc(params={"id": "A machine ID"})
class User(Resource):
    @jwt_required
    @users_ns.marshal_with(user_model)
    @users_ns.response(HTTPStatus.NOT_FOUND,
                       HTTPStatus.NOT_FOUND.phrase)
    def get(self, id):
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @jwt_required
    @users_ns.marshal_with(user_model)
    @users_ns.expect(user_parser)
    @users_ns.response(HTTPStatus.NOT_FOUND,
                       HTTPStatus.NOT_FOUND.phrase)
    def put(self):
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @jwt_required
    @users_ns.response(HTTPStatus.NOT_FOUND,
                       HTTPStatus.NOT_FOUND.phrase)
    def delete(self):
        abort(HTTPStatus.NOT_IMPLEMENTED)
