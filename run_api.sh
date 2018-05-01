#!/bin/sh
gunicorn shorty_api:shorty_api --log-file=-
