##from lxml import html
##import requests
##
##page = requests.get('http://onlinelibrary.wiley.com/doi/10.1002/asi.20045/abstract')
##tree = html.fromstring(page.content)
##links = tree.xpath('/a')
##print links
##
def get_full_urls(link,source_url):
    if 'http' in link:
        return link
    elif link[0] == '/':
        home = source_url.split('/')[2]
        return home+link
    else:
        print "suprising href: " + link
        return -1
            
    

import httplib2
from bs4 import BeautifulSoup, SoupStrainer


http = httplib2.Http()
status, response = http.request('http://onlinelibrary.wiley.com/doi/10.1002/asi.20045/abstract')

#get all unique links with the word pdf in them
soup = BeautifulSoup(response,'lxml');
links = soup.find_all('a')
pdfrefs = []
for link in links:
    ref = link.get('href')
    if 'pdf' in ref:
        pdfrefs.append(ref)

pdf_refs_unique = list(set(pdfrefs))
print pdf_refs_unique
for a in pdf_refs_unique: 
    print get_full_urls(a,'http://onlinelibrary.wiley.com/doi/10.1002/asi.20045/abstract')



    
##for link in soup.find_all('a')
##    print (link.get('href'))
##for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
##    if link.has_attr('href'):
##        print link['href']
