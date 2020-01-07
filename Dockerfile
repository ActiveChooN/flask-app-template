FROM python:3.7-alpine

ENV FLASK_CONFIG production

RUN mkdir /usr/src/app/

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev bash jpeg-dev zlib-dev tzdata libffi-dev \
    && apk add postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt

RUN ln -s /usr/share/zoneinfo/UTC /etc/localtime

COPY ./ /usr/src/app/

EXPOSE 80

CMD gunicorn --bind 0.0.0.0:80 -w 5 --log-level debug --timeout $WORKER_TIMEOUT -k gevent --preload manage:app