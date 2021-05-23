#!/bin/bash
cd /usr/src/app/mysite
# nohup uvicorn mysite.asgi:application --uds /tmp/uvicorn.sock > test.log &
poetry -h
#poetry shell

SOCKFILE=/usr/src/app/gunicorn.sock
# poetry run gunicorn mysite.wsgi:application --workers=2 --env DJANGO_SETTINGS_MODULE=mysite.settings --bind=unix:$SOCKFILE > test.log &
poetry run gunicorn mysite.wsgi:application --workers=2 --env DJANGO_SETTINGS_MODULE=mysite.settings --bind=0.0.0.0:8000 > test.log &
nginx

sleep 10000
while [[ true ]]; do
	sleep 10;
	echo "Test"
done