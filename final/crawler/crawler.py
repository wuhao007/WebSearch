###
### crawler.py
###
###

import json
from webcorpus import WebCorpus
from getpage import get_page, get_4sq_page
from bs4 import BeautifulSoup
import tweepy
import time
 
consumer_key = 'SXnbJLl01FUwbDdHhfLa1hEKL'
consumer_secret = 'aw98KXosbl4SCQoMXmVpHR0cEOsxnZriQZyNWPKdFtN3mgcQLN'
access_token = '35389991-nzPLU5KJxgWGMmFK9cqM1nT6iex2vpGRG2JGNIF7C'
access_token_secret = 'higyds4naaCTzWJz3oauzZ5CfzWC8is93FfIqKmFOq5Hy'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.me()
def put_venue(id):
    content = get_4sq_page('venues', id)
    venue = json.loads(content)['response']['venue']
    print '_'.join(venue['name'].split()), 
    location = venue['location']
#print '_'.join(location.values())
    print '_'.join([location['address'], location['crossStreet'], location['cc']])

def get_venue(page):
    soup = BeautifulSoup(page)
    try:
        for link in soup.find_all('meta'):
            href = link.get('content')
            if href.startswith('https://foursquare.com/v/'):
                put_venue(href.split('/')[-1])
                return
    except:
        pass
    return

def get_4sq(friend_twitter):
    print friend_twitter
    return [page.entities['urls'] for page in api.user_timeline(id=friend_twitter) if page.source == 'foursquare']

def get_all_friends(page):
    friends = []
    for group in json.loads(page)['response']['user']['friends']['groups']:
        for item in group['items']:
            friends.append(item['id'])
            if 'contact' in item and 'twitter' in item['contact']:
                try:
                    for t_urls in get_4sq(item['contact']['twitter']):
                        for t_url in t_urls:
                            print t_url['expanded_url']
                            get_venue(get_page(t_url['expanded_url']))
                except tweepy.TweepError:
                    time.sleep(60 * 15)
                    continue
                except StopIteration:
                    break
                except:
                    pass
    return friends

def crawl_web(seed):
    tocrawl = set([seed])
    crawled = []
    corpus = WebCorpus()
    while tocrawl:
        id = tocrawl.pop()
        if id not in crawled:
            content = get_4sq_page('users', id)
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
