# config
rename config-TEMPLATE.py to config.py and move to src and fill it with your info

# feedly_helper
this file work as init version. After filling the config file with your info run ```python3 feedly_helper.py``` it should return the request status as well as how many item was found as duplicate and marked read.  

# rssOptimizer
To optimize your rss feed. Removing duplicates and more.

### TODO
- [X] 3rd-party integration, feedly as a start
- [ ] convert feedly_helper.py to a class
- [ ] create a main in rssOptimizer.py to accept args
- [ ] keep track of all feeds in a local DB (tinyDB) to check if you ever read it before
- [ ] import opml
- [ ] create new feed after filter duplicates and filter
