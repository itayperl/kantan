# syntax=docker/dockerfile:1.3
FROM alpine AS builder

RUN apk add build-base
RUN apk update && apk add py3-pip linux-headers python3-dev pcre-dev git && \
    python3 -m venv  /venv
RUN mkdir /wheels && /venv/bin/pip install wheel && /venv/bin/pip wheel --no-deps uwsgi "git+https://github.com/fsan/python-romkan.git@d390d8ae1fd01ed692a1e28749d0214a9f237e5c" && \
    mv *.whl /wheels

FROM alpine

RUN apk update && apk add py3-pip pcre

COPY / /app
WORKDIR /app
RUN --mount=type=cache,ro,from=builder,source=/wheels,target=/wheels \
	python3 -m venv /venv && /venv/bin/pip install /wheels/* -r requirements.txt && rm -rf wheels

ENTRYPOINT /venv/bin/uwsgi --uid nobody --gid nobody --master -s 0.0.0.0:8080 --enable-threads --mount /=main:app
