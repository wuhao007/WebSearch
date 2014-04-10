###
### crawler.py
###
###

import json
from getpage import get_page

def get_all_friends(page):
    links = []
    #groups = json(page)['response']['user']['friends']['groups'][1]['items'][0]['id']
    for group in json.loads(page)['response']['user']['friends']['groups']:
        for item in group['items']:
            links.append(str(item['id']))
    return links

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = set([seed])
    crawled = []
    while tocrawl: 
        id = tocrawl.pop() # changed page to url - clearer name
        if id not in crawled:
            content = get_page(id)
            friends = get_all_friends(content)
            tocrawl.update(friends)
            crawled.append(id)
    return crawled
