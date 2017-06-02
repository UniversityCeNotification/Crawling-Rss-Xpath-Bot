""" Crawling url links """
import json
import os
import requests
import feedparser
from lxml import html
from pymongo import MongoClient
from dotenv import DotEnv
DOTENV = DotEnv('../.env')
CLIENT = MongoClient(DOTENV.get('MongoDbUri', 'mongodb://localhost:27017'))
DB = CLIENT[DOTENV.get('MongoDbName', 'rsscrawler')]  # which database
CRAWLERS = DB.crawlers  # which collection

class Bcolors:
    """ colorize the output """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def push_redis(data):
    """ pushing data to redis """
    return data

def write_file(data):
    """ writing data to file """
    return data

def insert_mongo_db(data):
    """ inserting data to mongodb """
    result = CRAWLERS.find_one({'link': data['link']})
    if not result:
        print(data)
        print('New Link crawled and inserted mongodb')
        CRAWLERS.insert_one(data)

def crawl_with_xpath(site_link, list_xpath, url_xpath, title_xpath, pubdate_xpath):
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
        insert_mongo_db(data)

    print(Bcolors.OKGREEN + '[-] Crawling Xpath Site Finished' + Bcolors.OKGREEN)

def crawl_with_rss(url):
    """ crawling with rss link """
    if url == '' or not url.startswith('http'):
        print(
            Bcolors.FAIL +
            'Error: url can not be empty string or url should startwith http' +
            Bcolors.ENDC
        )
        return
    rss = feedparser.parse(url)
    for entry in rss['entries']:
        data = {
            'title': entry['title'],
            'link': entry['link'],
            'pubdate': entry['updated'],
            'status': 'new'
        }
        insert_mongo_db(data)

    print(Bcolors.OKGREEN + '[-] Crawling Rss Site Finished' + Bcolors.ENDC)

if __name__ == '__main__':
    print(Bcolors.OKBLUE + '\n[*] Program Started' + Bcolors.ENDC)
    FILES = ['sites/'+ File for File in os.listdir('sites') if File.endswith('.json') and File != 'siteEmpty.json']
    print(FILES)
    for File in FILES:
        print(File)
        with open(File) as FileJsonData:
            site = json.load(FileJsonData)
            SiteName = site.get('SiteName', 'Nope')
            SiteLink = site.get('SiteLink', 'Nope')
            SiteRssLink = site.get('SiteRssLink', 'Nope')
            Xpath = site.get('Xpath', 'Nope')
            ListXpath = Xpath.get('ListXpath', 'Nope')
            UrlXpath = Xpath.get('UrlXpath', 'Nope')
            TitleXpath = Xpath.get('TitleXpath', 'Nope')
            PubDateXpath = Xpath.get('PubDateXpath', 'Nope')
            print(
                Bcolors.OKGREEN +
                '[+] Crawling Site:\n'+
                ' Name: ' + SiteName +
                ' | Link: ' + SiteLink +
                ' | RssLink: ' + SiteRssLink +
                Bcolors.ENDC
            )
            if not SiteRssLink == '':
                crawl_with_rss(SiteRssLink)
            else:
                crawl_with_xpath(SiteLink, ListXpath, UrlXpath, TitleXpath, PubDateXpath)
