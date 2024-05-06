#!/bin/bash

rm db.sqlite3
rm -rf ./cashflowapi/migrations
python3 manage.py makemigrations cashflowapi
python3 manage.py migrate
python3 manage.py migrate cashflowapi
python3 manage.py loaddata user token group team userteam category expense payment