import mwclient
import mwparserfromhell
import sys
import json
import unidecode
from bs4 import BeautifulSoup
from pymongo import MongoClient

useragent = "MW Database update bot 0.1, Run by Paul.Andrel@kantarmedia.com"
site = mwclient.Site('172.18.64.38', '/', clients_useragent=useragent)

site.login('pandrel', '4357pja')

#/ Set up an empty array to capture page list
#/ Process command line arguments into pages
pages = []
for arg in sys.argv:
    if arg == "process-page.py":
        continue
    if arg == "/home/pandrel/sitesheets-database/process-page.py":
        continue
    pages.append("Sitesheets:" + arg)

if pages == []:
    #We were called with no args pull from postgres
    import psycopg2
    conn = psycopg2.connect(database="oplogs", host="mwops.tnsmi-cmr.com", user="remote", password="littleblue")
    cursor = conn.cursor()
    cursor.execute("SELECT site FROM sitelist WHERE nonsite=false AND webremops=true ORDER BY site;")
    pgres = cursor.fetchall()
    for item in pgres:
        pages.append("Sitesheets:" + item[0])

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
            print "Skipping - " + item
            continue
        if ckey[0] != 'comments':
            item = soup.text
            key, value = item.split("=",1)
            value = value.rstrip('\n')
        else:
            key, value = item.split("=",1)
            value = value.rstrip('\n')
        data[key.strip()] = value.strip()
    client = MongoClient("mongodb://sitedata:Gibson9371@172.18.64.35/sitesheets")
    db = client.get_default_database()
    sitedata = db['sitedata']
    sitedata.delete_one({"site_id" : data[u"site_id"]})
    sitedata.insert_one(data)
    
for page in pages:
    mpage = site.Pages[page]
    text = mpage.text()
    if page == "Sitesheets:ONTO2":
        continue
    if page == "Sitesheets:ZDEV1":
        continue
    if page == "Sitesheets:ZDEV2":
        continue
    if page == "Sitesheets:ZDEV3":
        continue
    if page == "Sitesheets:ZFOP1":
        continue
    if page == "Sitesheets:ZFOP2":
        continue
    if page == "Sitesheets:DTV1":
        continue
    print "Processing - " + page + "."
    processPageText(text, page)
    print "Completed - " + page + "."
    
