import config
import opml
import feedparser

def opmlUrlParser():
    # return a dictionary (title,url)
    opmlFile = config.RSSOPT_CONFIG['opmlLocation']
    feeds = dict()
    rss = opml.parse(opmlFile)
    for i in range(0,len(rss)):
        for j in range(0,len(rss[i])):
            feeds[rss[i][j].title] = rss[i][j].xmlUrl
    return feeds
