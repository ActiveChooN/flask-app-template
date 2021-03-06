from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from flask_rbac import RBAC
from config import config
from celery import Celery

app = Flask(__name__)
mail = Mail()
cors = CORS(resources={r"/api/*": {"origins": "*"}})
cache = Cache()
celery = Celery()
jwt = JWTManager()
redis = FlaskRedis()
# rbac = RBAC()


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    cors.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)
    redis.init_app(app)
    # rbac.init_app(app)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    # celery.conf.update(app.config)

    from .api.v1 import blueprint as api
    app.register_blueprint(api, url_prefix="/api/v1")

    return app
