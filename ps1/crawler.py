###
### crawler.py
###
###

from getpage import get_page
from bs4 import BeautifulSoup
import urllib
from heapq import heappush, heappop, nsmallest
import re
from urlparse import urljoin
import time
import os

def get_all_link_keyword(page, url='', keyword = ''):
    soup = BeautifulSoup(page)
    links = []
    score = 0
    try:
        for key in keyword.split():
            score += len(soup.find_all(text=re.compile(key, re.IGNORECASE)))
        if score < 1:
            return links, score
        for link in soup.find_all('a'):
            outlink = str(link.get('href'))
            outlink = urljoin(url, outlink)
                #if url[-1] == '/' and outlink[0] == '/':
                #url = url[:-1]
                #outlink = (url + outlink).replace('\n', '').replace(' ', '')
            links += [outlink]
        #count = soup.find_all(text=re.compile(keyword))
        return links, score
    except:
        return links, score

def crawl_web(tocrawl, keyword, n = 1000): # returns index, graph of inlinks
    crawled = set([])
    url_finder = {}
    num_404 = 0
    total_size = 0
    fout = open('result.txt','w+')
    start = time.clock()
    while tocrawl: 
        url = heappop(tocrawl) # changed page to url - clearer name
        filehandle = get_page(url[1])
        if filehandle == None:
            continue
        code = filehandle.code
        if code == 404:
            num_404 += 1
        if code == 401:
            continue
        if filehandle.headers.type != 'text/html':
            continue
        new_url = filehandle.geturl()
        if new_url not in crawled:
            #corpus.add_page(url, new_url, outlinks, tocrawl, count)
            #tocrawl += outlinks
            page = filehandle.read()
            outlinks, count = get_all_link_keyword(page, new_url, keyword)
            if count == 0:
                continue
            len_tocrawl = len(tocrawl)
            for outlink in outlinks:
                is_new_link = True
                min_index = 0
                max_index = len_tocrawl - 1
                if outlink in url_finder:
                    key_score = url_finder[outlink]
                    while True:
                        if max_index < min_index:
                            break
                        m = (max_index + min_index)/2
                        target = tocrawl[m]
                        if target[0] < key_score:
                            min_index = m + 1
                        elif target[0] > key_score:
                            max_index = m - 1
                        else:
                            for j in range(min_index, max_index):
                                target = tocrawl[j]
                                if target[1] == outlink:
                                    is_new_link = False
                                    tocrawl.pop(j)
                                    url_score = target[0] - count
                                    heappush(tocrawl, (url_score, outlink))
                                    url_finder[outlink] = url_score
                                    break
                            break
#                for i in range(len_tocrawl):
#                    target = tocrawl[i]
#                    if target[1] == outlink:
#                        is_new_link = False
#                        tocrawl.pop(i)
#                        heappush(tocrawl, (target[0] - count, outlink))
#                        break
                #if is_new_link and len(tocrawl) < n:
                else:
                    heappush(tocrawl, (-count, outlink))
                    url_finder[outlink] = -count
            tocrawl = nsmallest(n, tocrawl)
            crawled.add(new_url)
            urllib.urlretrieve(new_url, os.path.join('downloads',str(n)+".html")) 
            n -= 1
            if n < 0:
                break
            size = len(page)
            total_size += size
            fout.write(new_url + ' time:' + str(time.clock()) + ' size:' + str(size) + ' return_code:' + str(code) + ' score:' + str(-url[0]) + ' actually:' + str(count) + '\n')

    fout.write('number_of_files:' + str(len(crawled)) + ' total_size:' + str(total_size) + ' total_time:' + str(time.clock() - start) + ' number_of_404_errors:' + str(num_404))
    fout.close()

    return crawled
