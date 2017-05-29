# Crawling-Rss-Bot
Crawling rss or site, and inserting mongodb or writing file or pushing redis.

If your site does not have rss, you should write [xpath](https://duckduckgo.com/?q=xpath+tutorial&t=ffab&ia=web)

# How to try this repo

```bash
  $ # Just run init.sh file
  $ bash init.sh          # Default, Crawler run every 60 second
  $ bash init.sh 10       # Crawler run every 10 second
```

# Example Json

```
{
  "Site": "Yildiz Teknik University",
  "SiteLink": "https://ytuce.maliayas.com/",
  "SiteRssLink": "https://ytuce.maliayas.com/?type=rss",
  "ListXpath": "//div[@class='text_title']",
  "UrlXpath": "a/@href",
  "TitleXpath": "a/text()"
}
```

<h4>University List or Site</h4>

|       University                                          |       Crawling Site                       |  Status  |
| --------------------------------------------------------- |:-----------------------------------------:|:--------:|
| [Yildiz Technical](https://www.ce.yildiz.edu.tr/)         |  https://ytuce.maliayas.com/?type=rss     |   Ok     |
| [Istanbul](http://ce.istanbul.edu.tr/)                    |  http://ce.istanbul.edu.tr/               |   Nope   |
| [Pamukkale](http://www.pamukkale.edu.tr/bilgisayar)       |  http://www.pamukkale.edu.tr/bilgisayar   |   WIP    |
| [Istanbul Technical](http://www.bb.itu.edu.tr/)           |  http://www.bb.itu.edu.tr/                |   Nope   |
| [Anadolu](https://anadolu.edu.tr)                         |  https://anadolu.edu.tr/duyurular         |   Nope   |
| [Reddit Python](https://www.reddit.com/r/Python/)         |  https://www.reddit.com/r/Python/.rss     |   Ok     |
