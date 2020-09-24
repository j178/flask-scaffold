FROM python:3.8-slim-buster as python-base

ENV LC_ALL C.UTF-8 \
    LANG C.UTF-8

WORKDIR /app
COPY . .

RUN echo "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib" > /etc/apt/sources.list \
    # uwsgi 需要
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y build-essential python-dev \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x -R ./scripts && scripts/install
CMD scripts/start
