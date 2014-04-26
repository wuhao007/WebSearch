###
### crawler.py
###
###

import json
from webcorpus import WebCorpus
from getpage import get_page

def get_all_friends(page):
    friends = []
    #groups = json(page)['response']['user']['friends']['groups'][1]['items'][0]['id']
    for group in json.loads(page)['response']['user']['friends']['groups']:
        for item in group['items']:
            friends.append(str(item['id']))
    return friends

def crawl_web(seed):
    tocrawl = set([seed])
    crawled = []
    corpus = WebCorpus()
    while tocrawl:
        id = tocrawl.pop()
        if id not in crawled:
            content = get_page(id)
            friends = get_all_friends(content)
            corpus.add_friend(id, friends)
            tocrawl.update(friends)
            crawled.append(id)
    return crawled

# def crawl_web(seed): # returns index, graph of inlinks
#     tocrawl = set([seed])
#     crawled = []
#     corpus = WebCorpus()
#     while tocrawl and len(crawled)<1000:
#         id = tocrawl.pop() # changed page to url - clearer name
#         if id not in crawled:
#             content = get_page(id)
#             friends = get_all_friends(content)
#             corpus.add_friend(id, friends)
#             tocrawl.update(friends)
#             crawled.append(id)
#     return crawled
