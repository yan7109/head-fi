# Create the database for headphones

import sqlite3
import string
from InitDatabase import *
from RssParser import *
from HTMLWriter import *
from CleanUpEntries import *
import time
import os.path

database_name = 'headphones.db'
init = True 
# Database already created
if os.path.isfile(database_name):
    init = False

conn = sqlite3.connect(database_name)
cur = conn.cursor()

# a dictionary for all known products
product_dict = {}

if init:
    product_dict = init_database(conn, cur)
else:
    product_dict = get_product_dict(conn, cur)


# Last stage, infinite loop for updating the database
while (True):
    query_rss_feed(conn, cur, product_dict)
    cleanup_inactive_entries(cur)
    conn.commit()
    port_to_html(cur)
    print "Last update at %s " % (datetime.datetime.now().time().isoformat())
    time.sleep(10)

conn.close()

