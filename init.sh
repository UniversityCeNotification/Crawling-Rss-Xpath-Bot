#!/bin/bash

read -p 'There is .env file in crawler?(y/n) : ' status
if [[ "$status" = "n" ]]; then
  read -p "MongoDbUrl:" url
  read -p "MongoDbName:" name
  echo "MongoDbUri='$url'" > .env
  echo "MongoDbName='$name'" >> .env
fi

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
while true
do
  python main.py
  sleep 60
done
deactivate
