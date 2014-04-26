###
### test.py
###

from crawler import crawl_web
from pygoogle import pygoogle
from heapq import heappush
import sys
from test import test

def test_engine():
    print "Testing..."

    keyword = 'NBA All-Star'
    n = 500
    if keyword.split() == []:
        print 'Please input something.'
   
    g = pygoogle(keyword)
    g.pages = 2
    tocrawl = []
    for url in g.get_urls()[0:10]:
        heappush(tocrawl, (-sys.maxint - 1, url))
    crawled = crawl_web(tocrawl, keyword, n)

    #print crawled
    #urls = rank_level_search(corpus, crawled)
    #for url in urls:
    #    print url
    print "Now finish crawling, please check the result in result.txt"

    print "The accururay rate is",test(keyword,n)

    print "Finished tests."

test_engine()
