FROM python:3.8-slim-buster as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIPENV_VENV_IN_PROJECT=1 \
    PIP_INDEX_URL="https://mirrors.aliyun.com/pypi/simple/" \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$VENV_PATH/bin:$PATH"

RUN python -m pip install -U wheel setuptools pip pipenv


# builder-base is used to build dependencies (such as uwsgi.)
FROM python-base as builder-base

# Install debs required by building uwsgi
RUN echo "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib" > /etc/apt/sources.list \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y build-essential python-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH
COPY ./Pipfile ./Pipfile.lock ./
# Install runtime deps only
RUN pipenv install --deploy


FROM python-base as development
ENV FLASK_ENV=development

# Copying venv into image
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR $PYSETUP_PATH
# venv already has runtime dpes installed, we got a quicker install
RUN pipenv install --dev

WORKDIR /app
COPY . .

EXPOSE 8000
ENTRYPOINT /docker-entrypoint.sh $0 $@
# Run a local development server
CMD ["flask", "run", "--reload", "--host=0.0.0.0", "--port=8000"]


FROM python-base as production
ENV FLASK_ENV=production

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY ./app /app
WORKDIR /app

ENTRYPOINT /docker-entrypoint.sh $0 $@
COPY ./etc/uwsgi.yaml /uwsgi.yaml
CMD ["uwsgi", "--yaml", "/uwsgi.yaml"]