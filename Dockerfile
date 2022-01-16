FROM docker.io/python:alpine

RUN apk update
RUN apk upgrade
RUN apk add libffi-dev gcc git python3-dev libjpeg-turbo-dev zlib-dev postgresql-dev libwebp-dev musl-dev libxml2-dev libxslt-dev neofetch

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN python3 -m venv /venv
RUN /venv/bin/pip3 install wheel

WORKDIR /opt/Clara
COPY requirements.txt .

RUN /venv/bin/pip3 install -U -r requirements.txt

COPY . .

CMD [ "sh", "-c", "source /venv/bin/activate; python -m SaitamaRobot" ]
