from flask import jsonify
from flask_restplus import Resource
from ...tasks import simple_task
from . import api


@api.route("/")
class Main(Resource):
    def get(self):
        result = simple_task.delay()
        return jsonify({"message": result.get(timeout=1)})
