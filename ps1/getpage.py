import urllib
import robotparser
from urlparse import urlparse

def get_page(url):
    try:
        url_ends = ('index.htm', 'index.html', 'index.jsp', 'main.html')
        for url_end in url_ends:
            i = -len(url_end)
            if url.find(url_end, i) != -1:
                url = url[:i-1]
        x_url_ends = ('pdf', 'javascript', 'img', 'gif', 'jsp')
        for x in x_url_ends:
            i = -len(x)
            if url.find(x, i) != -1:
                return None

        rp = robotparser.RobotFileParser()
        url_robot = url.split('/')
        o = urlparse(url)
        rp.set_url(o.scheme + '://' + o.netloc + '/robots.txt')
        rp.read()
        if rp.can_fetch("*", url) == False:
            return None
        return urllib.urlopen(url)
    except:
        return None
