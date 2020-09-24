FROM python:3.8

ENV LC_ALL C.UTF-8 \
    LANG C.UTF-8 \
    PIP_INDEX_URL="https://mirrors.aliyun.com/pypi/simple/" \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app
COPY . .

RUN chmod +x -R ./scripts && scripts/install
ENTRYPOINT scripts/start
