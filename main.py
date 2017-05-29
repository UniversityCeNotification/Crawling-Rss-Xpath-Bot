import json
import os

if __name__ == '__main__':
    Files = ['sites/'+ File for File in os.listdir('sites') if File.endswith('.json')]
    print(Files)
    for File in Files:
        with open(File) as FileJsonData:
            d = json.load(FileJsonData)
            print('[+] SiteName: ' + d.get('Site', 'Nope') + ' | SiteLink: ' + d.get('SiteLink', 'Nope') + ' | SiteRssLink: ' + d.get('SiteRssLink', 'Nope'))
