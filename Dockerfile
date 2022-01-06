FROM docker.io/python:alpine

RUN apk update
RUN apk upgrade
RUN apk add libffi-dev gcc git python3-dev libjpeg-turbo-dev zlib-dev postgresql-dev libwebp-dev musl-dev libxml2-dev libxslt-dev

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN python3 -m venv /venv
RUN /venv/bin/pip3 install wheel

COPY . /opt/Clara
WORKDIR /opt/Clara

RUN /venv/bin/pip3 install -U -r requirements.txt

CMD [ "sh", "-c", "source /venv/bin/activate; python -m SaitamaRobot" ]
