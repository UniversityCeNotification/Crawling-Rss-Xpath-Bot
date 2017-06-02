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

# Object Creator functions
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

def create_site_object(site):
    with open('../defaults/site.json') as empty_site_json:
        empty_site = json.load(empty_site_json)
        empty_site['SiteName'] = site.get('SiteName', '')
        empty_site['SiteLink'] = site.get('SiteLink', '')
        empty_site['SiteRssLink'] = site.get('SiteRssLink', '')
        empty_xpath = empty_site['Xpath']
        site_xpath = site.get('Xpath', {})
        empty_xpath['ListXpath'] = site_xpath.get('ListXpath', '')
        empty_xpath['UrlXpath'] = site_xpath.get('UrlXpath', '')
        empty_xpath['TitleXpath'] = site_xpath.get('TitleXpath', '')
        empty_xpath['PubDateXpath'] = site_xpath.get('PubDateXpath', '')
        return empty_site

# Writing Mongodb functions
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

		elif re.search('^/addsite (.*)$', msg['text']):
			site = {}
			site['SiteLink'] = re.search('^/addsite (.*)$', msg['text']).group(1)
			print(site)
			site = create_site_object(site)
			# Writing JSON data
			with open('../sites/site.json', 'w') as f:
				json.dump(site, f, indent=2)
			bot.sendMessage(chat_id, 'Added your site')
	else:
		print('not text')
# Main Section
if __name__ == '__main__':
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, handle).run_as_thread()
    print ('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)