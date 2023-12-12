#!/bin/bash

rm db.sqlite3
rm -rf ./playlistapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations playlistapi
python3 manage.py migrate playlistapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata creators
python3 manage.py loaddata friends
python3 manage.py loaddata episodes
python3 manage.py loaddata playlists
python3 manage.py loaddata tags
python3 manage.py loaddata episode_tags
# python3 manage.py loaddata
# python3 manage.py loaddata
