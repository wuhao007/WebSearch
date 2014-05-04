###
### crawler.py
###
###

import json
from webcorpus import WebCorpus
from getpage import get_page

import tweepy
 
consumer_key = 'SXnbJLl01FUwbDdHhfLa1hEKL'
consumer_secret = 'aw98KXosbl4SCQoMXmVpHR0cEOsxnZriQZyNWPKdFtN3mgcQLN'
access_token = '35389991-nzPLU5KJxgWGMmFK9cqM1nT6iex2vpGRG2JGNIF7C'
access_token_secret = 'higyds4naaCTzWJz3oauzZ5CfzWC8is93FfIqKmFOq5Hy'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.me()

def get_4sq(friend_twitter):
    return [page.entities['urls'] for page in api.user_timeline(id=friend_twitter) if page.source == 'foursquare']

def get_all_friends(page):
    friends = []
    #groups = json(page)['response']['user']['friends']['groups'][1]['items'][0]['id']
    for group in json.loads(page)['response']['user']['friends']['groups']:
        for item in group['items']:
            friends.append(str(item['id']))
            if 'contact' in item and 'twitter' in item['contact']:
                print get_4sq(item['contact']['twitter'])
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
