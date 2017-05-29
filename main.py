import json
import os
import feedparser

def crawl(url):
    d = feedparser.parse(url)
    for entry in d['entries']:
        print(entry['title'])
        print(entry['link'])

    print('[-] Crawling Site Finished')

if __name__ == '__main__':
    Files = ['sites/'+ File for File in os.listdir('sites') if File.endswith('.json')]
    print(Files)
    for File in Files:
        with open(File) as FileJsonData:
            d = json.load(FileJsonData)
            print('[+] Crawling, SiteName: ' + d.get('Site', 'Nope') + ' | SiteLink: ' + d.get('SiteLink', 'Nope') + ' | SiteRssLink: ' + d.get('SiteRssLink', 'Nope'))
            crawl(d.get('SiteRssLink', ''))
