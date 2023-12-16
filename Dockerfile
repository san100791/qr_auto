FROM python:3.11-alpine


# Add uwsgi user/group
RUN addgroup uwsgi
RUN adduser -D -h /home/uwsgi -G uwsgi uwsgi


RUN pip install --upgrade pip

# Update sources, install libs
RUN apk --update add --no-cache \
    libmemcached-dev \
    postgresql-libs \
    libuuid \
    pcre \
    libmagic

# Install build dependencies
ARG BUILD_DEPS=" \
    linux-headers \
    gcc \
    musl-dev \
    postgresql-dev \
    zlib-dev \
    openldap-dev \
    libldap \
    libsasl \
    apr-util-ldap \
    pcre-dev \
    libffi-dev"


RUN apk add --no-cache $BUILD_DEPS 
COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry install

COPY . .

EXPOSE 8000

COPY ./ /var/install/api

CMD ["gunicorn", "--config", "/var/install/api/gunicorn.conf.py", "finance_trade.api:app"]
