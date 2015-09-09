import mwclient
import sys
from pymongo import MongoClient

useragent = "MW Database update bot 0.1, Run by Paul.Andrel@kantarmedia.com"
site - mwclient.Site('172.18.64.38', '/index.php')

site.login('pandrel', '4357pja1')

#/ Set up an empty array to capture page list
pages = []
#/ Process commandline arguments into pages
for arg in sys.argv:
    pages.append(arg)
    
