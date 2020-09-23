FROM python:3.8

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENV PYPI_HOST "mirrors.aliyun.org"
ENV PYPI "http://mirrors.aliyun.org/pypi/simple"

WORKDIR /app
COPY  ./ ./

# 安装 pipenv
RUN pip install pipenv --no-cache-dir --index ${PYPI} --trusted-host ${PYPI_HOST}

# 使用 pipenv 安装依赖
RUN set -ex &&  pipenv install --system --deploy


# 暴露 gunicorn 监听的 5000 端口，link 容器间可以访问
EXPOSE 5000
