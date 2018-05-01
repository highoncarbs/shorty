#!/bin/sh
gunicorn app:app --log-file=-
