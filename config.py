import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    APP_MAIN_ADMIN = os.environ.get("ADMIN_LOGIN")
    APP_MAIN_ADMIN_PASS = os.environ.get("ADMIN_PASS")
    APP_SLOW_DB_QUERY_TIME = 0.3
    APP_NAME = os.environ.get("APP_NAME")
    APP_ROW_PER_PAGE = os.environ.get("APP_ROW_PER_PAGE") or 25
    APP_HOSTNAME = os.environ.get("APP_HOSTNAME") or "http://localhost:5000/"

    MAIL_USERNAME = os.environ.get("APP_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("APP_MAIL_PASSWORD")
    MAIL_SERVER = os.environ.get("APP_MAIL_SERVER")
    MAIL_PORT = os.environ.get("APP_MAIL_PORT")
    MAIL_USE_SSL = os.environ.get("APP_MAIL_USE_SSL")
    MAIL_SENDER = os.environ.get("APP_MAIL_SENDER")
    MAIL_ADMIN = os.environ.get("APP_MAIL_ADMINS")
    MAIL_SUBJECT_PREFIX = os.environ.get("APP_MAIL_SUBJECT_PREFIX")

    CACHE_TYPE = "null"
    CACHE_DEFAULT_TIMEOUT = 300

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
    CELERY_TASK_RESULT_EXPIRES = 3600
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'

    REDIS_URL = os.environ.get("REDIS_URL")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_DB")
    if os.environ.get("CACHE_REDIS_URL"):
        CACHE_TYPE = "redis"
        CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL")
    else:
        CACHE_TYPE = "simple"

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, "MAIL_USERNAME", None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, "MAIL_USE_TLS", None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.MAIL_ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + "Application error",
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # # handle reverse proxy server headers
        # from werkzeug.contrib.fixers import ProxyFix
        # app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    "testing": TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'unix': UnixConfig,
    "heroku": HerokuConfig,
}
