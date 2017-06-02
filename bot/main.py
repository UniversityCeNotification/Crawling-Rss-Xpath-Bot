import json
import re
import time
import telepot
from telepot.loop import MessageLoop
from dotenv import DotEnv
DOTENV = DotEnv('../.env')

TOKEN = DOTENV.get('TelegramToken', '') #sys.argv[1]  # get token from command-line

def create_user_object(who, date):
    with open('../defaults/user.json') as empty_user_json:
        user = json.load(empty_user_json)
        user['id'] = who['id']
        user['username'] = who['username']
        user['firstname'] = who['first_name']
        user['lastname'] = who['last_name']
        user['createdAt'] = date
        return user


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
         if re.search('^/start$', msg['text']):
            user = create_user_object(msg['from'], msg['date'])
            print(user)
            bot.sendMessage(chat_id, 'We create your account!')

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)

