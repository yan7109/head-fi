import sqlite3
import os 
import datetime

html_file_name = 'index_tmp.html'
homepage = 'index.html'

def port_to_html(cur):
    # Display top 10 bargains and prices
    outfile = open(html_file_name, 'w')
    current_time = datetime.datetime.now().time().isoformat()
    print >>outfile, """<html>
    <head>
    <title>HEAD-FI BARGAINS</title>
    <h1>HEAD-FI BARGAINS</h1>
    </head>
    <body>"""
    print >>outfile, "<br> Last updated at %s <br>" % (current_time)
    print >>outfile, """
    <table border="1">"""

    print >>outfile, "<tr><th>Product</th><th>Bargain Price</th><th>Average Price</th><th>Profit</th><th>Link</th></tr>"

    for row in cur.execute('select * from buy_list order by price_diff desc'):
        (product_id, product, average_price, num_active, num_total, price_diff, thread_id) = row
        if (thread_id != 0 and price_diff > 0): 
            bargain = average_price - price_diff
            link = "<a href=\"http://www.head-fi.org/t/" + str(thread_id) + "/\">link</a>"
            print >> outfile, "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( \
                product, bargain, average_price, price_diff, link) 

    print >>outfile, """</table>
    </body></html>"""

    outfile.close()
    os.system("mv %s %s" % (html_file_name, homepage))
