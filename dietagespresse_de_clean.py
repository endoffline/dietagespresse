# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:09:08 2018

@author: Andreas Stöckl
modified by Stefan Höller
"""

import sqlite3
import re
import pandas as pd

path = './db/dietagespressedata.db'
path_clean = './db/dietagespressedata_clean.db'
conn = sqlite3.connect(path_clean)
cur = conn.cursor()

def bereinigeReuters(txt):
    if txt != None:
        txt = re.sub("googletag.cmd.push.function.....googletag.display..div.banner.1.......","",txt)
        txt = re.sub("gbcallslot843.*..","",txt)

    return txt

def datumReuters(txt):
    if txt != None:

        txt = pd.to_datetime(txt)
    return str(txt)
    

conn2 = sqlite3.connect(path)
cur2 = conn2.cursor()

sqlstr = 'SELECT url,Kategorie,Titel,Body,Datum FROM Links'
for row in cur2.execute(sqlstr):
    if row[1] != None:
        cur.execute('''INSERT OR REPLACE INTO Artikel 
                (url,Kategorie,Titel,Body,Datum,Quelle,Fake) VALUES ( ?,?,?,?,?,?,? )''', (row[0],row[1],row[2],bereinigeReuters(row[3]),datumReuters(row[4]),"Reuters",0 ) )
conn.commit()    
cur2.close()
cur.close()