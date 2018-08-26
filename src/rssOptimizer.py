import config
import opml
import feedparser

def opml_url_parser():
    # return a dictionary (title,url)
    opmlFile = config.RSSOPT_CONFIG['OPML_LOCATION']
    feeds = dict()
    rss = opml.parse(opmlFile)
    for i in range(0,len(rss)):
        for j in range(0,len(rss[i])):
            feeds[rss[i][j].title] = rss[i][j].xmlUrl
    return feeds
