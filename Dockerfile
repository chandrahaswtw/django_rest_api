FROM python:3.13-alpine3.23
LABEL maintainer="www.chandrahasballeda.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    postgresql-dev \
    postgresql-client \
    musl-dev \
    jpeg-dev \
    zlib \
    zlib-dev

 
COPY ./requirements.txt .
COPY ./requirements.dev.txt .

ARG DEV=false

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        python -m pip install --no-cache-dir -r requirements.dev.txt; \
    fi

RUN adduser --disabled-password --no-create-home django-user

RUN mkdir -p /vol/web/media && \ 
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol 

USER django-user

COPY ./app /app

EXPOSE 8000