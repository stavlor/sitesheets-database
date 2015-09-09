import mwclient
import mwparserfromhell
import sys
from pymongo import MongoClient

useragent = "MW Database update bot 0.1, Run by Paul.Andrel@kantarmedia.com"
site = mwclient.Site('172.18.64.38', '/')

site.login('pandrel', '4357pja')

#/ Set up an empty array to capture page list
pages = ['Sitesheets:PAPH2']
#/ Process commandline arguments into pages
#for arg in sys.argv:
#    pages.append(arg)
#    print arg

def processPageText(text, page):
    wikicode = mwparserfromhell.parse(text)
    templates = wikicode.filter_templates()
    template = templates[0]
    for item in template.params:
        if item.startswith(u"<!-- "):
            continue
        item = item.rstrip('\n')
        print item

for page in pages:
    mpage = site.Pages[page]
    text = mpage.text()
    processPageText(text, page)
    
