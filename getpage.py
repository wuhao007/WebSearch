def real_get_page(id):
    import urllib
    print id
    url = 'https://api.foursquare.com/v2/users/' + id + '?v=040914&oauth_token=MGRUDACH5ZCGPSEA5PJIOH05UKOUT1WYMRNDIHPVX5GV0TMA'
    print url
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def get_page(url):
    return real_get_page(url)
