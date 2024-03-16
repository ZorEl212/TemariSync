#!/usr/bin/env bash
export  TEMP_DOC_DIR='/home/ubuntu/TemariSync/temp/'
export DOC_DIR='/home/ubuntu/TemariSync/docs/'
export RETURN_DIR='/home/ubuntu/TemariSync/return/'
export TS_ENV='dev'
export TS_DB='ts_dev_db'
export TS_DB_USER='ts_dev'
export TS_DB_PWD='ts_dev_pwd'
export TS_DB_HOST='localhost'
export STORAGE_TYPE='db'

python3 -m gunicorn --bind 0.0.0.0:5000 app:app

