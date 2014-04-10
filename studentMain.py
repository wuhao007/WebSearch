###
### test.py
###

from crawler import crawl_web
from search import lucky_search, ordered_search
import pickle

def test_engine():
    print "Testing..."
    kathleen = 'http://udacity.com/cs101x/urank/kathleen.html'
    nickel = 'http://udacity.com/cs101x/urank/nickel.html'
    arsenic = 'http://udacity.com/cs101x/urank/arsenic.html'
    hummus = 'http://udacity.com/cs101x/urank/hummus.html'
    indexurl = 'http://udacity.com/cs101x/urank/index.html'

    corpus = crawl_web('http://udacity.com/cs101x/urank/index.html')
    fname = 'corpus.pkl'

    # YOUR CODE HERE

    print lucky_search(corpus, 'Hummus') 
    print ordered_search(corpus, 'Hummus') 
    print lucky_search(corpus, 'the') 
    print ordered_search(corpus, 'the') 
    print lucky_search(corpus, 'babaganoush') 
    print ordered_search(corpus, 'babaganoush') 
    print "Finished tests."

test_engine()
