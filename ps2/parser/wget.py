import sys
from bs4 import BeautifulSoup
argv = sys.argv
f = open(argv[1], 'r')
soup = BeautifulSoup(f.read())
for link in soup.find_all('a'):
    print 'wget -c ' + argv[2] + link.get('href')
