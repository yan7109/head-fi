from Util import *
from DataInsertion import *
import sqlite3

def cleanup_inactive_entries(cur):
    
    key = (0,)
    for row in cur.execute("select * from buy_list where active_product_thread !=?", key):
        (product_id, name, average_price, num_active, num_total, price_diff, active_product_thread) = row
        url = get_url_from_thread_id(active_product_thread)
        is_active = is_active_thread(active_product_thread)
        if (is_active == False):
            key = (product_id, )
            agg_price = 0
            num_active = 0
            num_total = 0
            min_price = float('inf')
            min_product_thread = 0
            for raw_product in cur.execute("select * from raw_data where product_id =?", key):
                (o_active, o_thread_id, o_price, o_product, o_product_id) = raw_product
                
                agg_price = agg_price + o_price
                num_total = num_total + 1

                active = "inactive"
                if is_active_thread(o_thread_id): 
                    num_active = num_active + 1
                    active = "active"
                    if o_price < min_price:
                        min_price = o_price
                        min_product_thread = o_thread_id
                
                # The product is no longer active 
                if (active != o_active):
                    print "Updating thread to inactive"
                    print o_thread_id
                    insert_raw_data(active, o_thread_id, o_price, o_product, o_product_id, cur)

            key = (product_id, )
            cur.execute("select base_price from product_list where id=?", key)
            base_price = cur.fetchone()[0]
            laplace_smoothing = 10
            new_average_price = int((agg_price+base_price*laplace_smoothing)/(laplace_smoothing+num_total))
            # Everything is inactive
            if (min_price == float('inf')):
                new_price_diff = 0
            else:
                new_price_diff = new_average_price - min_price

            insert_buy_list(product_id, name, new_average_price, num_active, num_total, new_price_diff, min_product_thread, cur)
