#!/bin/bash

until nc -z ${RABBITMQ_HOST} ${RABBITMQ_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 1
done

until nc -z ${MONGO_HOST} ${MONGO_PORT}; do
    echo "$(date) - waiting for mongo..."
    sleep 1
done

python3 web.py
