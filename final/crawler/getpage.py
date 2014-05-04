import config

def get_page(id):
    import urllib2
    print id
    url = config.apiurl%id
    try:
        response =  urllib2.urlopen(url,timeout=3)
    except:
        print "Failed to open API response!"
        return ""
    return response.read()

