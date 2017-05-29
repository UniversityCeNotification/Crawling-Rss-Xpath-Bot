import json
import os
import feedparser
from pymongo import MongoClient
from dotenv import DotEnv
dotenv = DotEnv('.env')

client = MongoClient(dotenv.get('MongoDbUri', 'mongodb://localhost:27017'))
db = client[dotenv.get('MongoDbName', 'rsscrawler')] # which database
crawlers = db.crawlers  # which collection

def crawl(url):
    if url == '' or not url.startswith('http'):
        print('Error: url can not be empty string or url should startwith http')
        return
    d = feedparser.parse(url)
    for entry in d['entries']:
        data = {
            'title': entry['title'],
            'link': entry['link'],
            'status': 'new'
        }
        result = crawlers.find_one({'link': entry['link']})
        if not result:
            print('New Link crawled')
            crawlers.insert_one(data)

    print('[-] Crawling Site Finished')

if __name__ == '__main__':
    Files = ['sites/'+ File for File in os.listdir('sites') if File.endswith('.json')]
    print(Files)
    for File in Files:
        with open(File) as FileJsonData:
            d = json.load(FileJsonData)
            print('[+] Crawling, SiteName: ' + d.get('Site', 'Nope') + ' | SiteLink: ' + d.get('SiteLink', 'Nope') + ' | SiteRssLink: ' + d.get('SiteRssLink', 'Nope'))
            crawl(d.get('SiteRssLink', ''))
