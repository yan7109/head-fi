from lxml import html
import requests
from Util import *
from DataInsertion import *
import time

def parse_html(conn, cur, url, thread_id, product_dict):

    page = requests.get(url)
    tree = html.fromstring(page.text)

    category = tree.xpath('//span[@class="normal-txt"]/text()')[0]
    if (category == [] or str(category).lower() != "for sale: " and str(category).lower() != "for sale or trade: "): return
 
    currency = tree.xpath('//span[@class="currency"]/text()')
    if currency == []: return
    if currency[0] != '(USD)': return
           
    price = tree.xpath('//span[@class="ctx-price"]/text()')[0]
    if price == []: return
    if not isinstance(price[0], str): return
    price = int(remove_punctuations(str(price).split('.',1)[0]))
    # no outliers
    if price < 5 or price > 9999: return


    product = (tree.xpath('//span[@class="last"]/text()')[0]).lower()
    active = "active"
    if "sold" in product.split(): active = "inactive"
    closed = tree.xpath('//div[@class="closed"]/text()')
    if closed != []: active = "inactive"

    product = remove_punctuations(str(product))
    product = remove_stop_words(product)
    if product.lower() == '': return
    if len(product) > 30: product = product[:30]

    # Need a way to get the product id
    # passed in from the earlier flow
    
    unknown_product_id = product_dict['unknown']

    product_id = get_product_id(product_dict, product, unknown_product_id)

    # insert entry
    insert_raw_data(active, thread_id, price, product, product_id, cur)

    # update average price
    update_buy_list(product_id, unknown_product_id, active, thread_id, price, cur)    

    conn.commit()

