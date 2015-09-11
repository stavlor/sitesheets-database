import mwclient
import mwparserfromhell
import sys
import json
import unidecode
from bs4 import BeautifulSoup
from pymongo import MongoClient

useragent = "MW Database update bot 0.1, Run by Paul.Andrel@kantarmedia.com"
site = mwclient.Site('172.18.64.38', '/')

site.login('pandrel', '4357pja')

#/ Set up an empty array to capture page list
#/ Process commandline arguments into pages
pages = []
for arg in sys.argv:
    if arg == "process-page.py":
        continue
    if arg == "/home/pandrel/sitesheets-database/process-page.py":
        continue
    pages.append("Sitesheets:" + arg)

def processPageText(text, page):
    data = {}
    wikicode = mwparserfromhell.parse(text)
    templates = wikicode.filter_templates()
    template = templates[0]
    for item in template.params:
        item = unidecode.unidecode(item)
        soup = BeautifulSoup(item, "lxml")
        ckey = item.split("=", 1)
        if ckey[0].startswith("<!--"):
            continue
        if ckey[0] != 'comments':
            item = soup.text
            key, value = item.split("=",1)
            value = value.rstrip('\n')
        else:
            key, value = item.split("=",1)
            value = value.rstrip('\n')
        data[key.strip()] = value.strip()
#    print json.dumps(data)
#    print data[u"comm
    client = MongoClient("mongodb://sitedata:Gibson9371@172.18.64.35/sitesheets")
    db = client.get_default_database()
    sitedata = db['sitedata']
    sitedata.delete_one({"site_id" : data[u"site_id"]})
    sitedata.insert_one(data)
    
for page in pages:
    mpage = site.Pages[page]
    text = mpage.text()
    processPageText(text, page)
    
