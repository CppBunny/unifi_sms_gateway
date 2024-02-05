FROM --platform=$BUILDPLATFORM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt /app
RUN apk update
RUN apk add gcc
RUN apk add gcc musl-dev libffi-dev
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]
CMD ["sms.py"]