FROM python:3.8

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENV PYPI_HOST "mirrors.aliyun.org"
ENV PYPI "http://mirrors.aliyun.org/pypi/simple"

WORKDIR /app
COPY  ./ ./

RUN chmod +x -R ./scripts && scripts/install
ENTRYPOINT scripts/start
