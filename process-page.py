import mwclient
import mwparserfromhell
import sys
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

useragent = "MW Database update bot 0.1, Run by Paul.Andrel@kantarmedia.com"
site = mwclient.Site('172.18.64.38', '/')

site.login('pandrel', '4357pja')

#/ Set up an empty array to capture page list
pages = ['Sitesheets:AKFA1']
#/ Process commandline arguments into pages
#for arg in sys.argv:
#    pages.append(arg)
#    print arg

def processPageText(text, page):
    data = {}
    wikicode = mwparserfromhell.parse(text)
    templates = wikicode.filter_templates()
    template = templates[0]
    for item in template.params:
        item = str(item)
        soup = BeautifulSoup(item, "lxml")
        ckey = item.split("=", 1)
        if ckey[0] != 'comments':
            item = soup.text
            key, value= item.split("=",1)
            value = value.rstrip('\n')
        else:
            key, value = item.split("=",1)
            value = value.rstrip('\n')
        data[key.strip()] = value.strip()
    print json.dumps(data)
    print data[u"comments"]

for page in pages:
    mpage = site.Pages[page]
    text = mpage.text()
    processPageText(text, page)
    
