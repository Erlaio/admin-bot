# Stage 1: Prepare base image
FROM python:3.8-alpine3.15 as base

ENV CRYPTOGRAPHY_DONT_BUILD_RUST = 1

# Stage 2: Prepare Python virtual Environment
FROM base as builder

RUN apk add --no-cache build-base \
                       linux-headers \
                       musl-dev \
                       libffi-dev \
                       openssl-dev \
                       make \
                       postgresql-dev \
                       libxml2-dev \
                       libxslt-dev


RUN pip install poetry

COPY . /src/

WORKDIR /src

RUN python -m venv /env && . /env/bin/activate && pip install --upgrade pip && pip install wheel && poetry install

# Stage 3: Build admin-bot container
FROM base

RUN apk add --no-cache postgresql-libs

COPY --from=builder /env /env

COPY . /src/

RUN mkdir -p /db

WORKDIR /src

CMD ["/env/bin/python3", "app.py"]

