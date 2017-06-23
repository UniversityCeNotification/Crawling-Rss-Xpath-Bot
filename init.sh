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

# Started Bot
cd bot
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py &
deactivate
cd -

# Notification start
cd notification
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py &
deactivate
cd -

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
