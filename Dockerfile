FROM docker.io/python:3.10-alpine AS base

RUN apk update
RUN apk upgrade
RUN apk add libjpeg-turbo-dev

WORKDIR /opt/Clara

FROM base AS builder

RUN apk add gcc git libffi-dev libwebp-dev python3-dev musl-dev libxml2-dev libxslt-dev

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN python3 -m venv /venv
RUN /venv/bin/pip3 install wheel

COPY requirements.txt .

RUN /venv/bin/pip3 install -U -r requirements.txt

FROM base AS deployment

RUN apk add postgresql neofetch
	
COPY --from=builder /venv /venv
COPY . .

CMD [ "sh", "-c", "source /venv/bin/activate; python -m SaitamaRobot" ]
