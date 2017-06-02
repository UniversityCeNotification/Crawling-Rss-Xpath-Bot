import json
import re
import time
import telepot
from telepot.loop import MessageLoop
from dotenv import DotEnv
from pymongo import MongoClient

# Constants
DOTENV = DotEnv('../.env')
CLIENT = MongoClient(DOTENV.get('MongoDbUri', 'mongodb://localhost:27017'))
DB = CLIENT[DOTENV.get('MongoDbName', 'rsscrawler')]  # which database
CRAWLERS = DB.crawlers  # which collection
USERS = DB.users  # which collection

TOKEN = DOTENV.get('TelegramToken', '') #sys.argv[1]  # get token from command-line

# Functions
def create_user_object(who, date):
    """ creating user object from empty user.json """
    with open('../defaults/user.json') as empty_user_json:
        user = json.load(empty_user_json)
        user['id'] = who['id']
        user['username'] = who['username']
        user['firstname'] = who['first_name']
        user['lastname'] = who['last_name']
        user['createdAt'] = date
        return user

def insert_user_mongo_db(user):
    """ inserting user to mongodb """
    result = USERS.find_one({'username': user['username']})
    if not result:
        print(user)
        print('New User added!')
        USERS.insert_one(user)
        return 1
    return -1

# Telebot handle function
def handle(msg):
    """ handling telegram messages """
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
         if re.search('^/start$', msg['text']):
            user = create_user_object(msg['from'], msg['date'])
            result = insert_user_mongo_db(user)
            if result == 1:
                bot.sendMessage(chat_id, 'We create your account!')
            else:
                bot.sendMessage(chat_id, 'You already have a account!')

# Main Section
if __name__ == '__main__':
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, handle).run_as_thread()
    print ('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)