import json
import re
import time
import requests
import feedparser
import io
from lxml import html
from urllib.parse import urljoin
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

def get_empty_site_object():
    with open('../defaults/site.json') as empty_site_json:
        empty_site = json.load(empty_site_json)
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

# Deleting Mongodb functions
def delete_user_mongo_db(username):
    USERS.remove({'username': username})

def feedfinder(url):
    """ https://gist.github.com/pleycpl/46953ff26e7da165c9f20dfbe1cd8256 """
    print(url)
    raw = False
    try:
        raw = requests.get(url, timeout=10.0).content
    except Exception as e:
        return 'Website doesn\'t exists.'

    if not raw:
        return 'Lxml doesn\'t work.'

    result = []
    possibleFeeds = []
    tree = html.fromstring(raw)
    feedUrls = tree.xpath("//link[@rel='alternate']")
    if feedUrls:
        for feed in feedUrls:
            t = feed.xpath('@type')
            if t:
                t = t[0]
                if "rss" in t or "xml" in t:
                    href = feed.xpath('@href')
                    if href:
                        href = href[0]
                        possibleFeeds.append(urljoin(url, href))

    atags = tree.xpath("//a")
    for a in atags:
        href = a.xpath('@href')
        if href:
            href = href[0]
            if "xml" in href or "rss" in href or "feed" in href:
                possibleFeeds.append(urljoin(url, href))

    for link in list(set(possibleFeeds)):
        # Thanks for https://stackoverflow.com/questions/9772691/feedparser-with-timeout
        try:
            resp = requests.get(link, timeout=10.0)
        except Exception as e:
            print("Timeout when reading RSS %s", link, ' e:', e)
            continue

        content = io.BytesIO(resp.content)

        f = feedparser.parse(content)
        if len(f.entries) > 0:
            if url not in result:
                result.append(link)

    site = {}
    site['SiteName'] = tree.xpath('//title/text()')[0]
    site['SiteRssLink'] = result[0] if len(result) > 0 else ''
    return site


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
            link = re.search('^/addsite (.*)$', msg['text']).group(1)
            result = feedfinder(link)
            if isinstance(result, str):
                bot.sendMessage(chat_id, result)
                return
            
            site = get_empty_site_object()
            site['SiteLink'] = link
            site['SiteName'] = result['SiteName']
            site['SiteRssLink'] = result['SiteRssLink']
            jsonname = site['SiteLink'].replace('https://', '').replace('http://', '').replace('.', '_').replace('/', '_')
            print(site)
            print(jsonname)
            # Writing JSON data
            with open('../sites/' + jsonname + '.json', 'w') as f:
                json.dump(site, f, indent=2)

            if site['SiteRssLink'] == '':
                bot.sendMessage(chat_id, 'Please insert xpath for this site,like \n/updatesite listxpath <site-name>')
            else:
                bot.sendMessage(chat_id, 'Added your site')
        
        elif re.search('^/deleteme$', msg['text']):
            delete_user_mongo_db(msg['from']['username'])
            bot.sendMessage(chat_id, 'Deleted your account!')

        else:
            bot.sendMessage(chat_id, msg['text'] + ' What are you saying?')
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