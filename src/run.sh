#!/bin/bash

docker-compose down
docker-compose rm
docker-compose build
docker-compose up -d db
sleep 30*1000
docker-compose up web

