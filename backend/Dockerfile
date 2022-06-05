# syntax=docker/dockerfile:1.3
FROM alpine AS builder

RUN apk add build-base
RUN apk update && apk add py3-pip linux-headers python3-dev pcre-dev
RUN mkdir /wheels && pip3 install wheel && pip3 wheel --no-deps uwsgi && \
    mv uWSGI*.whl /wheels

FROM alpine

RUN apk update && apk add py3-pip pcre

COPY / /app
WORKDIR /app
RUN --mount=type=cache,ro,from=builder,source=/wheels,target=/wheels \
	pip3 install /wheels/* -r requirements.txt && rm -rf wheels

ENTRYPOINT uwsgi --uid nobody --gid nobody --master -s 0.0.0.0:8080 --enable-threads --mount /=main:app
