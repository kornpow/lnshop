##### BUILDER IMAGE #####
# FROM bitnami/minideb:latest
# FROM debian:stretch-slim
FROM alpine:edge

RUN mkdir -p /usr/src/app

# RUN install_packages \
# RUN apk update && apk add \
# 	python3 \
# 	python3-dev \
# 	python3-pip \
# 	python3-venv \
# 	git \
# 	nginx \
# 	gcc \
# 	libevent-dev \
# 	curl \ 
# 	procps \
# 	nano

RUN apk update && apk add --no-cache \
	python3 \
	python3-dev \
	py3-pip \
	git \
	nginx \
	gcc \
	g++ \
	libgcc \
	make \
	libevent-dev \
	curl \ 
	procps \
	nano \
	musl-dev \
	libffi-dev \
	openssl-dev \
	zlib-dev \
	jpeg-dev \
	zlib-dev \
	freetype-dev \
	lcms2-dev \
	openjpeg-dev \
	tiff-dev \
	tk-dev \
	tcl-dev

# RUN useradd -d /usr/src/app lapp && chown -R lapp /usr/src/app/
RUN addgroup -S lapp && adduser -S lapp -G lapp -h /usr/src/app && chown -R lapp /usr/src/app/
WORKDIR /usr/src/app
RUN chown -R lapp:lapp /var/log
USER lapp


# Install poetry python package managaer
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
ENV PATH "/usr/src/app/.poetry/bin:${PATH}"
RUN poetry self update --preview

COPY --chown=lapp:lapp poetry.lock .
COPY --chown=lapp:lapp  pyproject.toml .
RUN poetry install -vvv

USER root
RUN mkdir /db && chown -R lapp:lapp /db
VOLUME /db


USER lapp
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


ENV BUMPIP 0.0.4

COPY config/nginx.conf /etc/nginx/nginx.conf
COPY --chown=lapp:lapp mysite ./mysite

COPY --chown=lapp:lapp start.sh /usr/src/app/start.sh

RUN mkdir -p /usr/src/app/db && mkdir -p /usr/src/app/static

ENV MAC {ADD HEX ENCODED MACAROON HERE}
ENV TLS {ADD HEX ENCODED TLS CERT HERE}

ENV NODE_IP={ADD NODE IP ADDRESS HERE}

# EXPOSE 8000 80
# EXPOSE 3000 3000
EXPOSE 8000

CMD ["/bin/sh","./start.sh"]
