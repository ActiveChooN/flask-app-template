FROM python:3.7

ENV FLASK_CONFIG production

RUN mkdir /usr/src/app/

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN apt-get update \
    && apt-get install python3-dev \
    && pip install --no-cache-dir -r requirements.txt

RUN ln -s /usr/share/zoneinfo/UTC /etc/localtime

COPY ./ /usr/src/app/

EXPOSE 80

CMD gunicorn --bind 0.0.0.0:80 -w $WORKERS_NUM --log-level debug --timeout $WORKER_TIMEOUT -k gevent --preload manage:app