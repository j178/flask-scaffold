#!/usr/bin/env bash

while true; do
    if flask db upgrade; then
        break
    fi

    echo Deploy command failed, retrying in 5 secs
    sleep 5
done

flask translate compile
exec gunicorn wsgi:app -c ./etc/gunicorn.conf.py
