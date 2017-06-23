""" Crawling url links """
import json
import os
import requests
import feedparser
from lxml import html
from pymongo import MongoClient
from dotenv import DotEnv
from util.bcolors import Bcolors

### Global Variables
DOTENV = DotEnv('../.env')
CLIENT = MongoClient(DOTENV.get('MongoDbUri', 'mongodb://localhost:27017'))
DB = CLIENT[DOTENV.get('MongoDbName', 'rsscrawler')]  # which database
CRAWLERS = DB.crawlers  # which collection
SITES_DIRECTORY = '../sites/'

def push_redis(data):
    """ pushing data to redis """
    return data

def write_file(data):
    """ writing data to file """
    return data

def insert_mongo_db(isinit, data, siteurl):
    """ inserting data to mongodb """
    if not data == {}:
        result = CRAWLERS.find_one({'link': data['link']})
        if not result:
            print('New Link crawled and inserted mongodb')
            print(data)
            data['siteurl'] = siteurl
            if isinit == 'True':
                data['status'] = 'old'
            CRAWLERS.insert_one(data)

def crawl_with_xpath(isinit, site_link, list_xpath, url_xpath, title_xpath, pubdate_xpath):
    """ crawling url with xpaths """
    page = requests.get(site_link)
    tree = html.fromstring(page.content)
    items = tree.xpath(list_xpath)
    for item in items:
        url = item.xpath(url_xpath)[0]
        title = item.xpath(title_xpath)[0]
        pubdate = item.xpath(pubdate_xpath)[0]
        data = {
            'title': title,
            'link': url,
            'pubdate': pubdate,
            'status': 'new'
        }
        insert_mongo_db(isinit, data, site_link)

def get_value_in_dict(d, *args):
    for arg in args:
        try:
            return d[arg]
        except:
            print(arg)
            continue

def general_rss_content_parse(entry):
    return {
        'title': get_value_in_dict(entry, 'title'),
        'link': get_value_in_dict(entry, 'link'),
        'pubdate': get_value_in_dict(entry, 'updated', 'summary'),
        'status': 'new'
    }

def crawl_with_rss(isinit, rssurl, siteurl):
    """ crawling with rss link """
    if rssurl == '' or not rssurl.startswith('http'):
        print(Bcolors.FAIL('Error: url can not be empty string or url should startwith http'))
        return
    rss = feedparser.parse(rssurl)
    for entry in rss['entries']:
        data = general_rss_content_parse(entry)
        insert_mongo_db(isinit, data, siteurl)

if __name__ == '__main__':
    print(Bcolors.OKBLUEFUNC('\n[*] Program Started'))
    FILES = [SITES_DIRECTORY + File for File in os.listdir(SITES_DIRECTORY) if File.endswith('.json')]
    print(FILES)
    for File in FILES:
        print(File)
        with open(File) as FileJsonData:
            site = json.load(FileJsonData)
            print(site)
            print(Bcolors.OKGREENFUNC('[+] Crawling Site:\n Name: {} | Link: {} | RssLink: {}'.format(site['SiteName'], site['SiteLink'], site['SiteRssLink'])))
            if not site['SiteRssLink'] == '':
                crawl_with_rss(site['Init'], site['SiteRssLink'], site['SiteLink'])
                print(Bcolors.OKGREENFUNC('[-] Crawling Rss Site Finished'))
            else:
                crawl_with_xpath(site['Init'], site['SiteLink'], site['Xpath']['ListXpath'], site['Xpath']['UrlXpath'], site['Xpath']['TitleXpath'], site['Xpath']['PubDateXpath'])
                print(Bcolors.OKGREENFUNC('[-] Crawling Xpath Site Finished'))

            if site['Init'] == 'True':
                site['Init'] = 'False'
                with open(File, 'w') as f:
                    json.dump(site, f, indent=2)