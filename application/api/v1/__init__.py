from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint("api", __name__)
api = Api(blueprint, version="1.0", title="Template Flask App", doc="/swagger",
          description="Template flask application with REST-API")


from . import main, api_models
from .auth import auth_ns
from .users import users_ns

api.add_namespace(auth_ns)
api.add_namespace(users_ns)
