FROM python:3.8-alpine

# -- timezone sync
RUN set -ex && apk update \
    && apk add tzdata \
    && cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && echo "Asia/Seoul" > /etc/timezone \
    && apk del tzdata

# build-base: gevent dependency
# libffi-dev: bcrypt dependency
RUN set -ex && apk update \
    && apk add build-base libffi-dev \
    && rm -rf /var/cache/apk/*

# centos7에서 pip upgrade 중 EnvironmentError [Errno 39] “Directory not empty” 발생
# RUN set -ex \
#     && pip3 install --upgrade pip
# && pip3 install pipenv

RUN mkdir /code
WORKDIR /code


# -- add dependency list for pipenv
# ONBUILD COPY Pipfile Pipfile
# ONBUILD COPY Pipfile.lock Pipfile.lock

# -- create .venv in WORKDIR
# ENV PIPENV_VENV_IN_PROJECT=.
# ONBUILD RUN set -ex && pipenv sync --dev

# -- install dependency with pip
ONBUILD COPY requirements.txt requirements.txt
ONBUILD RUN set -ex & pip install -r requirements.txt
# -- Install Application into container:
ONBUILD COPY src src