# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:55:01 2018

@author: Andreas Stöckl
modified by Stefan Höller
"""
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
ctx.headers = {'User-Agent': 'Mozilla/5.0'}

import sqlite3
path = './db/dietagespressedata.db'
conn = sqlite3.connect(path)
cur = conn.cursor()


for i in range(1,33):
    url = 'https://dietagespresse.com/page/' + str(i)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    teaser = soup.find_all("h2", class_="entry-title")
    for art in teaser:
        link = art.find("a")
        link = link.get('href')
        cur.execute('''INSERT OR IGNORE INTO Links (url) VALUES ( ? )''', (link, ) )
conn.commit()
cur.close()


def loadArtikelTagespresse(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    kat = soup.find_all("p", class_="bb-cat-links")
    
    if kat != []:
        kat = kat[0].get_text()
    else:
        return None    
    date = soup.find_all("time", itemprop="datePublished")
    
    if date != []:
        date = date[0]['datetime']
    else:
        return None
    title = soup.find_all("h1", class_="entry-title")
 
    if title != []:
        title = title[0].get_text()
    else:
        return None
    body = soup.find_all("div", class_="s-post-content")

    if body != []:
        body = body[0].get_text()
    else:
        return None
    cur.execute('''INSERT OR REPLACE INTO Links (url,Kategorie,Titel, Body, Datum, crawled) VALUES (?,?,?,?,?,?)''', (url,kat,title,body,date,"1" ) )
    return None

conn = sqlite3.connect(path)
cur = conn.cursor()

cur.execute('SELECT url,crawled FROM Links')
sel = cur.fetchmany(400)
for row in sel:
    if row[1] != "1":
        loadArtikelTagespresse(row[0])
conn.commit()
cur.close()
