import sqlite3

def insert_raw_data(active, thread_id, price, product, product_id, cur):
    insertion = 'insert or replace into raw_data(active, thread_id, price, product, product_id) values ' \
                + str('(\'') + str(active) + str('\', ') \
                + str(thread_id) + str(', ') + str(price) \
                + str(', \'') + str(product) + str('\', ') \
                + str(product_id) + str(');')
    cur.execute(insertion)


def insert_buy_list(product_id, known_product_name, average_price, num_active, num_total, price_diff, product_thread, cur):
    insertion = 'insert or replace into buy_list(id, name, average_price, num_active, num_total, price_diff, active_product_thread) values ' \
                + str('(') + str(product_id) \
                + str(', \'') + str(known_product_name) + str('\', ') \
                + str(average_price) + str(', ') \
                + str(num_active) + str(', ') + str(num_total)  + str(', ') \
                + str(price_diff) + str(', ') + str(product_thread) \
                + str(');')

    
    print insertion
    cur.execute(insertion)


def update_buy_list(product_id, unknown_product_id, active, thread_id, price, cur):
    # Populate the to buy list
    if product_id != unknown_product_id:
        # check if product is already in buy list
        key = (product_id, )
        cur.execute('select * from buy_list where id=?', key)
        exist = cur.fetchone()
        cur.execute('select * from product_list where id=?', key)
        (temp_key, known_product_name, base_price) = cur.fetchone()
        laplace_smooth = 10

        # The item doesn't exist
        if exist == None:
            average_price = int((base_price*laplace_smooth+price)/(laplace_smooth+1))
            price_diff = 0 # price diff = 0 for inactive items
            num_active = 0
            product_thread = 0
            num_total = 1
            if active == 'active':
                num_active = 1
                product_thread = thread_id
                price_diff = average_price - price # bigger delta the better

        else:
            (o_product_id, o_product_name, o_average_price, o_num_active, o_num_total, o_price_diff, o_product_thread) = exist
            average_price = int((o_average_price*(laplace_smooth+o_num_total)+price)/(laplace_smooth+o_num_total+1))
            num_total = o_num_total + 1
            num_active = o_num_active
            product_thread = o_product_thread
            price_diff = 0

            if num_active > 0:
                price_diff = average_price - (o_average_price - o_price_diff)

            if active == 'active':
                num_active = o_num_active+1
                if average_price - price > o_price_diff or product_thread == 0:
                    price_diff = average_price - price
                    product_thread = thread_id

        # Anything selling for 20% of retail price is bogus
        threshold_price_diff = 0.80
        # The price difference cannot be below threshold
        if float(price_diff)/float(average_price) > threshold_price_diff:
            return

        insert_buy_list(product_id, known_product_name, average_price, num_active, num_total, price_diff, product_thread, cur)
