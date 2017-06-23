import schedule
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

SITES_DIRECTORY = '../sites/'
DEFAULTS_DIRECTORY = '../defaults/'

def job():
    print("I'm working...", time.strftime('%X %x %Z'))

if __name__ == '__main__':
    bot = telepot.Bot(TOKEN)
    schedule.every(1).minutes.do(job)
    i = 0
    while True:
        print("Loop ", i)
        schedule.run_pending()
        time.sleep(10)
        i += 1