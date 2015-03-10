import feedparser
import sqlite3
import re
from HTMLParser import *

def query_rss_feed(conn, cur, product_dict):

    rss_url = "http://www.head-fi.org/rss.php?action=livefeed&forumId=6550"
    feed = feedparser.parse(rss_url)
    for entry in feed['entries']:
        url = entry['links'][0]['href']
        thread_id = (re.search('\/t\/(.+?)\/',str(url))).group(1)

        # check if thread id exists in database
        key = (thread_id, )
        cur.execute('select * from raw_data where thread_id = ?', key)
        exist = cur.fetchone()
        # Need to update the database 
        if exist == None:
            # scrape html, and update the database
            parse_html(conn, cur, url, thread_id, product_dict)
