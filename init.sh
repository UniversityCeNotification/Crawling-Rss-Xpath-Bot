#!/bin/bash

# Checking parameter
if [ "$1" = "" ]
then
    time=60
else
    time=$1
fi

echo $time "second"

# Checking .env file
read -p 'There is .env file in crawler?(y/n) : ' status
if [[ "$status" = "n" ]]; then
  read -p "MongoDbUrl:" url
  read -p "MongoDbName:" name
  read -p "TelegramToken:" token
  echo "MongoDbUri='$url'" > .env
  echo "MongoDbName='$name'" >> .env
  echo "TelegramToken='$token'" >> .env
fi

function start_python_code_background {
  cd $1
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python main.py &
  deactivate
  cd -
}

# Bot start
start_python_code_background bot

# Notification start
start_python_code_background notification

# Crawling start
cd crawler
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
while true
do
  python main.py
  sleep $time
done
deactivate
