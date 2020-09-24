FROM python:3.8

ENV LC_ALL C.UTF-8 \
    LANG C.UTF-8

WORKDIR /app
COPY . .

RUN chmod +x -R ./scripts && scripts/install
CMD scripts/start
