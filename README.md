# Crawling-Rss-Bot
Crawling rss or site, and inserting mongodb or writing file or pushing redis.

If your site does not have rss, you should write [xpath](https://duckduckgo.com/?q=xpath+tutorial&t=ffab&ia=web)

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
