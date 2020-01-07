from . import celery


@celery.task
def simple_task():
    return "Hello, world!"
